"""Authentication schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request with username/email and password."""

    username: str = Field(..., min_length=1, description="Username or email")
    password: str = Field(..., min_length=1, description="Password")


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token expiration in seconds")


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class RoleResponse(BaseModel):
    """Role response model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class UserResponse(BaseModel):
    """User response model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    active: bool
    confirmed_at: datetime | None = None
    roles: list[RoleResponse] = []


class UserCreate(BaseModel):
    """User creation request."""

    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6)
    roles: list[str] = Field(default_factory=list)


class UserUpdate(BaseModel):
    """User update request."""

    username: str | None = Field(None, min_length=3, max_length=80)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)
    active: bool | None = None
    roles: list[str] | None = None
