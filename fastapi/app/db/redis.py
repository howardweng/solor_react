"""Async Redis connection management with graceful error handling."""
import json
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import ConnectionError, TimeoutError, RedisError

from app.core.config import settings
from app.core.exceptions import RedisConnectionError

logger = logging.getLogger(__name__)


class RedisManager:
    """Manages async Redis connections for main and GTR servers with graceful error handling."""

    def __init__(self):
        self._pools: dict[str, ConnectionPool] = {}
        self._clients: dict[str, Redis] = {}
        self._connection_status: dict[str, bool] = {}

    def _create_pool(self, host: str, port: int, password: str, db: int = 0) -> ConnectionPool:
        """Create a Redis connection pool."""
        return ConnectionPool(
            host=host,
            port=port,
            password=password or None,
            db=db,
            decode_responses=True,
            max_connections=20,
            socket_timeout=5.0,  # 5 second timeout
            socket_connect_timeout=5.0,
        )

    def get_main_pool(self) -> ConnectionPool:
        """Get or create the main Redis connection pool."""
        if "main" not in self._pools:
            self._pools["main"] = self._create_pool(
                host=settings.redis_host,
                port=settings.redis_port,
                password=settings.redis_password,
                db=settings.redis_db,
            )
        return self._pools["main"]

    def get_gtr_pool(self) -> ConnectionPool:
        """Get or create the GTR Redis connection pool."""
        if "gtr" not in self._pools:
            self._pools["gtr"] = self._create_pool(
                host=settings.redis_host_gtr,
                port=settings.redis_port_gtr,
                password=settings.redis_password_gtr,
            )
        return self._pools["gtr"]

    def get_main_client(self) -> Redis:
        """Get Redis client for main server."""
        if "main" not in self._clients:
            self._clients["main"] = Redis(connection_pool=self.get_main_pool())
        return self._clients["main"]

    def get_gtr_client(self) -> Redis:
        """Get Redis client for GTR server."""
        if "gtr" not in self._clients:
            self._clients["gtr"] = Redis(connection_pool=self.get_gtr_pool())
        return self._clients["gtr"]

    def is_connected(self, server: str = "main") -> bool:
        """Check if Redis server is connected."""
        return self._connection_status.get(server, False)

    async def check_connection(self, server: str = "main") -> bool:
        """Test Redis connection and return status."""
        try:
            client = self.get_main_client() if server == "main" else self.get_gtr_client()
            await client.ping()
            self._connection_status[server] = True
            return True
        except (ConnectionError, TimeoutError, RedisError) as e:
            self._connection_status[server] = False
            logger.warning(f"Redis '{server}' connection check failed: {e}")
            return False

    async def health_check(self) -> dict[str, bool]:
        """Check all Redis connections and return status dict."""
        return {
            "main": await self.check_connection("main"),
            "gtr": await self.check_connection("gtr"),
        }

    async def close_all(self) -> None:
        """Close all Redis connections."""
        for client in self._clients.values():
            await client.close()
        for pool in self._pools.values():
            await pool.disconnect()
        self._clients.clear()
        self._pools.clear()
        self._connection_status.clear()


# Global Redis manager instance
redis_manager = RedisManager()


@asynccontextmanager
async def get_redis_safe() -> AsyncGenerator[Redis | None, None]:
    """
    Get main Redis client with graceful error handling.

    Yields None if Redis is unavailable.
    """
    client = redis_manager.get_main_client()
    try:
        await client.ping()
        redis_manager._connection_status["main"] = True
        yield client
    except (ConnectionError, TimeoutError, RedisError) as e:
        redis_manager._connection_status["main"] = False
        logger.warning(f"Redis main connection failed: {e}")
        yield None


@asynccontextmanager
async def get_redis_gtr_safe() -> AsyncGenerator[Redis | None, None]:
    """
    Get GTR Redis client with graceful error handling.

    Yields None if Redis is unavailable.
    """
    client = redis_manager.get_gtr_client()
    try:
        await client.ping()
        redis_manager._connection_status["gtr"] = True
        yield client
    except (ConnectionError, TimeoutError, RedisError) as e:
        redis_manager._connection_status["gtr"] = False
        logger.warning(f"Redis GTR connection failed: {e}")
        yield None


async def get_redis() -> AsyncGenerator[Redis | None, None]:
    """Dependency for getting main Redis client (graceful - returns None on failure)."""
    async with get_redis_safe() as client:
        yield client


async def get_redis_gtr() -> AsyncGenerator[Redis | None, None]:
    """Dependency for getting GTR Redis client (graceful - returns None on failure)."""
    async with get_redis_gtr_safe() as client:
        yield client


async def get_redis_required() -> AsyncGenerator[Redis, None]:
    """Dependency for getting main Redis client (raises on failure)."""
    client = redis_manager.get_main_client()
    try:
        await client.ping()
        redis_manager._connection_status["main"] = True
        yield client
    except (ConnectionError, TimeoutError, RedisError) as e:
        redis_manager._connection_status["main"] = False
        raise RedisConnectionError(f"Redis is unavailable: {e}")


async def redis_scan(
    redis: Redis | None,
    pattern: str,
    count: int = 100,
) -> list[dict[str, Any]]:
    """
    Scan Redis keys matching a pattern and return their values.

    Returns empty list if Redis is unavailable.
    """
    if redis is None:
        logger.warning("Redis unavailable, returning empty result for scan")
        return []

    results = []
    cursor = 0

    try:
        while True:
            cursor, keys = await redis.scan(cursor=cursor, match=pattern, count=count)

            for key in keys:
                key_type = await redis.type(key)

                if key_type == "hash":
                    data = await redis.hgetall(key)
                    results.append(data)
                elif key_type == "string":
                    value = await redis.get(key)
                    try:
                        data = json.loads(value) if value else {}
                        results.append(data)
                    except json.JSONDecodeError:
                        results.append({"value": value})

            if cursor == 0:
                break
    except (ConnectionError, TimeoutError, RedisError) as e:
        logger.warning(f"Redis scan failed: {e}")
        return []

    return results


async def redis_get_hash(redis: Redis | None, key: str) -> dict[str, Any]:
    """Get a hash from Redis. Returns empty dict if unavailable."""
    if redis is None:
        return {}
    try:
        data = await redis.hgetall(key)
        return data
    except (ConnectionError, TimeoutError, RedisError) as e:
        logger.warning(f"Redis get hash failed for '{key}': {e}")
        return {}


async def redis_get_json(redis: Redis | None, key: str) -> dict[str, Any] | None:
    """Get a JSON value from Redis. Returns None if unavailable."""
    if redis is None:
        return None
    try:
        value = await redis.get(key)
        if value is None:
            return None
        return json.loads(value)
    except json.JSONDecodeError:
        return None
    except (ConnectionError, TimeoutError, RedisError) as e:
        logger.warning(f"Redis get JSON failed for '{key}': {e}")
        return None


async def redis_set_with_fallback(
    redis: Redis | None,
    key: str,
    value: Any,
    ex: int | None = None,
) -> bool:
    """
    Set a value in Redis with fallback behavior.

    Returns True if successful, False if Redis is unavailable.
    """
    if redis is None:
        logger.warning(f"Redis unavailable, cannot set key '{key}'")
        return False
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await redis.set(key, value, ex=ex)
        return True
    except (ConnectionError, TimeoutError, RedisError) as e:
        logger.warning(f"Redis set failed for '{key}': {e}")
        return False
