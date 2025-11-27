"""Main API router combining all v1 routes."""
from fastapi import APIRouter

from . import auth, system, bess, pcs, meters, inverter, schedule, analysis, config

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(bess.router, prefix="/bess", tags=["bess"])
api_router.include_router(pcs.router, prefix="/pcs", tags=["pcs"])
api_router.include_router(meters.router, prefix="/meters", tags=["meters"])
api_router.include_router(inverter.router, prefix="/inverter", tags=["inverter"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
