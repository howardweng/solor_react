"""Async database session management for multiple databases."""
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Literal

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.exceptions import DatabaseConnectionError

logger = logging.getLogger(__name__)

# Database identifiers
DatabaseName = Literal[
    "ess", "schedule", "meter", "pcs", "inverter", "baseline",
    "bess1", "bess2", "bess3", "bess4", "bess5", "bess6",
    "bess7", "bess8", "bess9", "bess10", "bess11", "bess12",
]


class DatabaseManager:
    """Manages multiple async database connections with graceful error handling."""

    def __init__(self):
        self._engines: dict[str, AsyncEngine] = {}
        self._session_factories: dict[str, async_sessionmaker[AsyncSession]] = {}
        self._connection_status: dict[str, bool] = {}

    def _get_database_url(self, db_name: DatabaseName) -> str:
        """Get database URL for a specific database."""
        url_map = {
            "ess": settings.database_url_ess,
            "schedule": settings.database_url_schedule,
            "meter": settings.database_url_meter,
            "pcs": settings.database_url_pcs,
            "inverter": settings.database_url_inverter,
            "baseline": settings.database_url_baseline,
        }

        if db_name in url_map:
            return url_map[db_name]

        # Handle BESS databases (bess1-bess12)
        if db_name.startswith("bess"):
            bess_num = int(db_name[4:])
            return settings.get_bess_database_url(bess_num)

        raise ValueError(f"Unknown database: {db_name}")

    def _create_engine(self, db_name: DatabaseName) -> AsyncEngine:
        """Create an async engine for a database."""
        url = self._get_database_url(db_name)
        return create_async_engine(
            url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,
            connect_args={"connect_timeout": 5},  # 5 second timeout
        )

    def get_engine(self, db_name: DatabaseName) -> AsyncEngine:
        """Get or create an engine for a database."""
        if db_name not in self._engines:
            self._engines[db_name] = self._create_engine(db_name)
        return self._engines[db_name]

    def get_session_factory(
        self, db_name: DatabaseName
    ) -> async_sessionmaker[AsyncSession]:
        """Get or create a session factory for a database."""
        if db_name not in self._session_factories:
            engine = self.get_engine(db_name)
            self._session_factories[db_name] = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
        return self._session_factories[db_name]

    def is_connected(self, db_name: DatabaseName) -> bool:
        """Check if database is connected."""
        return self._connection_status.get(db_name, False)

    @asynccontextmanager
    async def session(
        self, db_name: DatabaseName, required: bool = True
    ) -> AsyncGenerator[AsyncSession | None, None]:
        """
        Context manager for database sessions with graceful error handling.

        Args:
            db_name: Database to connect to
            required: If True, raise exception on connection failure.
                     If False, yield None and continue gracefully.
        """
        factory = self.get_session_factory(db_name)
        try:
            async with factory() as session:
                # Test connection
                await session.execute(text("SELECT 1"))
                self._connection_status[db_name] = True
                try:
                    yield session
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise
        except OperationalError as e:
            self._connection_status[db_name] = False
            logger.warning(f"Database '{db_name}' connection failed: {e}")
            if required:
                raise DatabaseConnectionError(
                    f"Database '{db_name}' is unavailable. Please try again later."
                )
            yield None
        except SQLAlchemyError as e:
            self._connection_status[db_name] = False
            logger.error(f"Database '{db_name}' error: {e}")
            if required:
                raise DatabaseConnectionError(f"Database error: {e}")
            yield None

    @asynccontextmanager
    async def optional_session(
        self, db_name: DatabaseName
    ) -> AsyncGenerator[AsyncSession | None, None]:
        """
        Context manager that yields None if database is unavailable.

        Use this for non-critical operations where you want to continue
        even if the database is down.
        """
        async with self.session(db_name, required=False) as session:
            yield session

    async def check_connection(self, db_name: DatabaseName) -> bool:
        """Test database connection and return status."""
        try:
            async with self.session(db_name, required=True):
                return True
        except DatabaseConnectionError:
            return False

    async def health_check(self) -> dict[str, bool]:
        """Check all database connections and return status dict."""
        status = {}
        for db_name in ["ess", "schedule", "meter", "pcs", "inverter", "baseline"]:
            status[db_name] = await self.check_connection(db_name)
        return status

    async def close_all(self) -> None:
        """Close all database connections."""
        for engine in self._engines.values():
            await engine.dispose()
        self._engines.clear()
        self._session_factories.clear()
        self._connection_status.clear()


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_session(
    db_name: DatabaseName = "ess",
) -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a database session (raises on failure)."""
    async with db_manager.session(db_name, required=True) as session:
        yield session


async def get_optional_db_session(
    db_name: DatabaseName = "ess",
) -> AsyncGenerator[AsyncSession | None, None]:
    """Dependency for getting an optional database session (returns None on failure)."""
    async with db_manager.session(db_name, required=False) as session:
        yield session


# Shortcut dependencies for common databases
async def get_ess_session() -> AsyncGenerator[AsyncSession, None]:
    """Get ESS database session."""
    async for session in get_db_session("ess"):
        yield session


async def get_schedule_session() -> AsyncGenerator[AsyncSession, None]:
    """Get Schedule database session."""
    async for session in get_db_session("schedule"):
        yield session


async def get_meter_session() -> AsyncGenerator[AsyncSession, None]:
    """Get Meter database session."""
    async for session in get_db_session("meter"):
        yield session


async def get_pcs_session() -> AsyncGenerator[AsyncSession, None]:
    """Get PCS database session."""
    async for session in get_db_session("pcs"):
        yield session


async def get_inverter_session() -> AsyncGenerator[AsyncSession, None]:
    """Get Inverter database session."""
    async for session in get_db_session("inverter"):
        yield session


# Optional session dependencies (graceful failure)
async def get_optional_ess_session() -> AsyncGenerator[AsyncSession | None, None]:
    """Get optional ESS database session."""
    async for session in get_optional_db_session("ess"):
        yield session


async def get_optional_meter_session() -> AsyncGenerator[AsyncSession | None, None]:
    """Get optional Meter database session."""
    async for session in get_optional_db_session("meter"):
        yield session
