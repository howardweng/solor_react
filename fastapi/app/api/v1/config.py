"""Configuration endpoints."""
from fastapi import APIRouter
from sqlalchemy import select, func

from app.api.deps import EssSession
from app.core.config import settings
from app.models.alert import AlertLog
from app.schemas.config import (
    SidebarInfoResponse,
    HeaderInfoResponse,
    AlertSummary,
)

router = APIRouter()


@router.get("/sidebar", response_model=SidebarInfoResponse)
async def get_sidebar_info():
    """
    Get sidebar configuration information.

    Equivalent to Flask /api/sidebar_info

    Returns system configuration for sidebar display.
    """
    number_of_devices = (
        settings.bess_number +
        settings.pcs_number +
        settings.inverter_number +
        settings.rack_number
    )

    return SidebarInfoResponse(
        bess_type=settings.bess_type,
        bess_number=settings.bess_number,
        pcs_number=settings.pcs_number,
        inverter_number=settings.inverter_number,
        rack_number=settings.rack_number,
        number_of_devices=number_of_devices,
        cctv_url=settings.cctv_url or None,
    )


@router.get("/header", response_model=HeaderInfoResponse)
async def get_header_info(db: EssSession = None):
    """
    Get header alert summary.

    Equivalent to Flask /api/header_info

    Returns counts and lists of unsolved alerts by level:
    - Protection (critical)
    - Warning
    - Fault
    """
    protection_info = AlertSummary(count=0, items=[])
    warning_info = AlertSummary(count=0, items=[])
    fault_info = AlertSummary(count=0, items=[])

    if db:
        # Query unsolved alerts grouped by level
        # Protection level
        protection_result = await db.execute(
            select(AlertLog)
            .where(AlertLog.level == "protection")
            .where(AlertLog.solved == False)
        )
        protection_alerts = protection_result.scalars().all()
        protection_info = AlertSummary(
            count=len(protection_alerts),
            items=[f"{a.device}: {a.condition}" for a in protection_alerts[:10]],
        )

        # Warning level
        warning_result = await db.execute(
            select(AlertLog)
            .where(AlertLog.level == "warning")
            .where(AlertLog.solved == False)
        )
        warning_alerts = warning_result.scalars().all()
        warning_info = AlertSummary(
            count=len(warning_alerts),
            items=[f"{a.device}: {a.condition}" for a in warning_alerts[:10]],
        )

        # Fault level
        fault_result = await db.execute(
            select(AlertLog)
            .where(AlertLog.level == "fault")
            .where(AlertLog.solved == False)
        )
        fault_alerts = fault_result.scalars().all()
        fault_info = AlertSummary(
            count=len(fault_alerts),
            items=[f"{a.device}: {a.condition}" for a in fault_alerts[:10]],
        )

    return HeaderInfoResponse(
        protection_info=protection_info,
        warning_info=warning_info,
        fault_info=fault_info,
    )
