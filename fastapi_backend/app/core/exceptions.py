"""Custom exception handlers and HTTP exceptions."""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class SolarHubException(Exception):
    """Base exception for SolarHub application."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseConnectionError(SolarHubException):
    """Raised when database connection fails."""

    def __init__(self, message: str = "Database connection failed"):
        super().__init__(message, status_code=503)


class RedisConnectionError(SolarHubException):
    """Raised when Redis connection fails."""

    def __init__(self, message: str = "Redis connection failed"):
        super().__init__(message, status_code=503)


class AuthenticationError(SolarHubException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(SolarHubException):
    """Raised when user lacks permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class NotFoundError(SolarHubException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status_code=404)


class ValidationError(SolarHubException):
    """Raised when validation fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)


# HTTP Exception shortcuts
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

permission_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough permissions",
)

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found",
)


async def solarhub_exception_handler(
    request: Request, exc: SolarHubException
) -> JSONResponse:
    """Handle SolarHub custom exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "detail": None,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc) if request.app.state.debug else None,
        },
    )
