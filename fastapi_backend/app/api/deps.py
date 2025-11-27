"""API dependencies for dependency injection."""
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import verify_token
from app.db.session import get_db_session, db_manager
from app.db.redis import get_redis, get_redis_gtr
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User | None:
    """
    Get the current authenticated user from JWT token.

    Returns None if no token or invalid token (for optional auth).
    """
    if token is None:
        return None

    payload = verify_token(token, token_type="access")
    if payload is None:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    async with db_manager.session("ess") as session:
        result = await session.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        return user


async def get_current_active_user(
    current_user: Annotated[User | None, Depends(get_current_user)],
) -> User:
    """
    Get the current authenticated and active user.

    Raises 401 if not authenticated or user is inactive.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return current_user


async def get_optional_user(
    current_user: Annotated[User | None, Depends(get_current_user)],
) -> User | None:
    """
    Get the current user if authenticated, otherwise None.

    Use this for endpoints that work with or without authentication.
    """
    return current_user


# Type aliases for dependency injection
CurrentUser = Annotated[User, Depends(get_current_active_user)]
OptionalUser = Annotated[User | None, Depends(get_optional_user)]
RedisClient = Annotated[Redis, Depends(get_redis)]
RedisGTRClient = Annotated[Redis, Depends(get_redis_gtr)]


# Database session dependencies
async def get_ess_db() -> AsyncGenerator[AsyncSession, None]:
    """Get ESS database session."""
    async with db_manager.session("ess") as session:
        yield session


async def get_schedule_db() -> AsyncGenerator[AsyncSession, None]:
    """Get Schedule database session."""
    async with db_manager.session("schedule") as session:
        yield session


async def get_meter_db() -> AsyncGenerator[AsyncSession, None]:
    """Get Meter database session."""
    async with db_manager.session("meter") as session:
        yield session


async def get_pcs_db() -> AsyncGenerator[AsyncSession, None]:
    """Get PCS database session."""
    async with db_manager.session("pcs") as session:
        yield session


async def get_inverter_db() -> AsyncGenerator[AsyncSession, None]:
    """Get Inverter database session."""
    async with db_manager.session("inverter") as session:
        yield session


async def get_baseline_db() -> AsyncGenerator[AsyncSession, None]:
    """Get Baseline database session."""
    async with db_manager.session("baseline") as session:
        yield session


# Type aliases for database sessions
EssSession = Annotated[AsyncSession, Depends(get_ess_db)]
ScheduleSession = Annotated[AsyncSession, Depends(get_schedule_db)]
MeterSession = Annotated[AsyncSession, Depends(get_meter_db)]
PcsSession = Annotated[AsyncSession, Depends(get_pcs_db)]
InverterSession = Annotated[AsyncSession, Depends(get_inverter_db)]
BaselineSession = Annotated[AsyncSession, Depends(get_baseline_db)]
