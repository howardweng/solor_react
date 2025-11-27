"""FastAPI application entry point."""
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    app.state.debug = settings.debug
    yield
    # Shutdown
    await db_manager.close_all()
    await redis_manager.close_all()


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
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SolarHub API",
        "version": "1.0.0",
    }
