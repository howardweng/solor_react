"""Async Redis connection management."""
import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio import ConnectionPool, Redis

from app.core.config import settings


class RedisManager:
    """Manages async Redis connections for main and GTR servers."""

    def __init__(self):
        self._pools: dict[str, ConnectionPool] = {}
        self._clients: dict[str, Redis] = {}

    def _create_pool(self, host: str, port: int, password: str, db: int = 0) -> ConnectionPool:
        """Create a Redis connection pool."""
        return ConnectionPool(
            host=host,
            port=port,
            password=password or None,
            db=db,
            decode_responses=True,
            max_connections=20,
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

    async def close_all(self) -> None:
        """Close all Redis connections."""
        for client in self._clients.values():
            await client.close()
        for pool in self._pools.values():
            await pool.disconnect()
        self._clients.clear()
        self._pools.clear()


# Global Redis manager instance
redis_manager = RedisManager()


async def get_redis() -> AsyncGenerator[Redis, None]:
    """Dependency for getting main Redis client."""
    client = redis_manager.get_main_client()
    try:
        yield client
    finally:
        pass  # Connection managed by pool


async def get_redis_gtr() -> AsyncGenerator[Redis, None]:
    """Dependency for getting GTR Redis client."""
    client = redis_manager.get_gtr_client()
    try:
        yield client
    finally:
        pass  # Connection managed by pool


async def redis_scan(
    redis: Redis,
    pattern: str,
    count: int = 100,
) -> list[dict[str, Any]]:
    """
    Scan Redis keys matching a pattern and return their values.

    Equivalent to the Flask RedisScan utility but async.
    """
    results = []
    cursor = 0

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

    return results


async def redis_get_hash(redis: Redis, key: str) -> dict[str, Any]:
    """Get a hash from Redis."""
    data = await redis.hgetall(key)
    return data


async def redis_get_json(redis: Redis, key: str) -> dict[str, Any] | None:
    """Get a JSON value from Redis."""
    value = await redis.get(key)
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None
