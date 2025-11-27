"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    SolarHubException,
    generic_exception_handler,
    solarhub_exception_handler,
)
from app.db.session import db_manager
from app.db.redis import redis_manager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting SolarHub API...")
    app.state.debug = settings.debug

    # Check connections on startup (non-blocking)
    logger.info("Checking database connections...")
    db_status = await db_manager.health_check()
    for db_name, connected in db_status.items():
        status = "connected" if connected else "unavailable"
        logger.info(f"  Database '{db_name}': {status}")

    logger.info("Checking Redis connections...")
    redis_status = await redis_manager.health_check()
    for server, connected in redis_status.items():
        status = "connected" if connected else "unavailable"
        logger.info(f"  Redis '{server}': {status}")

    logger.info("SolarHub API started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down SolarHub API...")
    await db_manager.close_all()
    await redis_manager.close_all()
    logger.info("SolarHub API shutdown complete.")


app = FastAPI(
    title="SolarHub API",
    description="IoT Dashboard API for Solar Energy Storage Systems",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "auth", "description": "Authentication operations"},
        {"name": "system", "description": "System overview and topology"},
        {"name": "bess", "description": "Battery Energy Storage System"},
        {"name": "pcs", "description": "Power Conversion System"},
        {"name": "meters", "description": "Power meters and readings"},
        {"name": "inverter", "description": "Inverter data"},
        {"name": "schedule", "description": "Energy trading schedule"},
        {"name": "income", "description": "Income and revenue"},
        {"name": "analysis", "description": "Power analysis and reporting"},
        {"name": "config", "description": "System configuration"},
        {"name": "admin", "description": "Admin operations"},
    ],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(SolarHubException, solarhub_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["health"])
async def root():
    """Root endpoint."""
    return {
        "service": "SolarHub API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Basic health check endpoint.

    Returns healthy if the API is running, regardless of database/Redis status.
    Use /health/detailed for full infrastructure status.
    """
    return {
        "status": "healthy",
        "service": "SolarHub API",
        "version": "1.0.0",
    }


@app.get("/health/detailed", tags=["health"])
async def detailed_health_check():
    """
    Detailed health check with infrastructure status.

    Returns status of all databases and Redis connections.
    The API can still function with some services unavailable.
    """
    # Check database connections
    db_status = await db_manager.health_check()
    db_healthy = any(db_status.values())  # At least one DB connected

    # Check Redis connections
    redis_status = await redis_manager.health_check()
    redis_healthy = any(redis_status.values())  # At least one Redis connected

    # Overall status
    overall_status = "healthy" if (db_healthy or redis_healthy) else "degraded"
    if not db_healthy and not redis_healthy:
        overall_status = "unhealthy"

    return {
        "status": overall_status,
        "service": "SolarHub API",
        "version": "1.0.0",
        "infrastructure": {
            "databases": {
                "status": "healthy" if db_healthy else "unhealthy",
                "connections": db_status,
            },
            "redis": {
                "status": "healthy" if redis_healthy else "unhealthy",
                "connections": redis_status,
            },
        },
        "message": (
            "All systems operational"
            if overall_status == "healthy"
            else "Some services are unavailable, API may have limited functionality"
        ),
    }


@app.get("/health/live", tags=["health"])
async def liveness_check():
    """
    Kubernetes liveness probe endpoint.

    Returns 200 if the application is running.
    """
    return {"status": "alive"}


@app.get("/health/ready", tags=["health"])
async def readiness_check():
    """
    Kubernetes readiness probe endpoint.

    Returns 200 if at least one database is connected.
    Returns 503 if no databases are available.
    """
    db_status = await db_manager.health_check()
    if any(db_status.values()):
        return {"status": "ready"}

    # Return 503 if no databases available
    from fastapi import Response
    return Response(
        content='{"status": "not ready", "reason": "No database connections"}',
        status_code=503,
        media_type="application/json",
    )
