"""Authentication service."""
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User, Role
from app.schemas.auth import TokenResponse, UserCreate


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
) -> User | None:
    """Authenticate user by username/email and password."""
    # Try to find by username or email
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where((User.username == username) | (User.email == username))
    )
    user = result.scalar_one_or_none()

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user


async def create_tokens(user: User) -> TokenResponse:
    """Create access and refresh tokens for a user."""
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Get user by ID with roles loaded."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user."""
    # Get roles
    roles = []
    if user_data.roles:
        result = await db.execute(
            select(Role).where(Role.name.in_(user_data.roles))
        )
        roles = list(result.scalars().all())

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password),
        active=True,
        roles=roles,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
