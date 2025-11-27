"""Common base schemas for API responses."""
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseResponse(BaseModel):
    """Base response model with status."""

    model_config = ConfigDict(from_attributes=True)

    status: str = "success"


class MessageResponse(BaseResponse):
    """Response with a message."""

    message: str


class StatusResponse(BaseResponse):
    """Response with status and optional data."""

    data: dict[str, Any] | None = None
    message: str | None = None


class DataResponse(BaseResponse, Generic[T]):
    """Generic response with typed data."""

    data: T


class PaginatedResponse(BaseResponse, Generic[T]):
    """Paginated response with items."""

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


class ErrorResponse(BaseModel):
    """Error response model."""

    status: str = "error"
    message: str
    detail: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str
