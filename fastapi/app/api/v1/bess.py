"""BESS (Battery Energy Storage System) endpoints."""
from typing import Any

from fastapi import APIRouter, Path, HTTPException

from app.api.deps import RedisClient, RedisGTRClient
from app.core.config import settings
from app.db.redis import redis_scan
from app.schemas.bess import BessInfoResponse, RackAlertResponse

router = APIRouter()


@router.get("/{bess_number}", response_model=BessInfoResponse)
async def get_bess_info(
    bess_number: int = Path(..., ge=1, le=12, description="BESS unit number (1-12)"),
    redis: RedisGTRClient = None,
):
    """
    Get BESS unit information.

    Equivalent to Flask /api/bams_info/<bess_number>

    Returns rack data including:
    - Mode, Voltage, Current, Power, Temperature
    - SOC%, SOH%, Cell voltage/temperature differences
    """
    # Table headers (rack IDs)
    table_head = [f"Rack {i:02d}" for i in range(1, settings.rack_number + 1)]

    # Metrics rows
    metrics = [
        "Mode",
        "Voltage (V)",
        "Current (A)",
        "Power (kW)",
        "Temperature (°C)",
        "SOC (%)",
        "SOH (%)",
        "Max Cell Voltage (V)",
        "Min Cell Voltage (V)",
        "Max Cell Temp (°C)",
        "Min Cell Temp (°C)",
        "Cell Voltage Diff (V)",
        "Cell Temp Diff (°C)",
    ]

    # Build data rows (in production, fetch from Redis)
    data = []
    for metric in metrics:
        row: dict[str, Any] = {"metric": metric}
        for i in range(1, settings.rack_number + 1):
            rack_key = f"Rack {i:02d}"
            # Placeholder - in production, fetch actual values
            row[rack_key] = "N/A"
        data.append(row)

    return BessInfoResponse(
        bess_number=bess_number,
        table_head=table_head,
        data=data,
    )


@router.get("/alert/rack/{rack_number}", response_model=RackAlertResponse)
async def get_rack_alert(
    rack_number: str = Path(
        ...,
        pattern=r"^rack(0[1-9]|1[0-2])$",
        description="Rack identifier (rack01-rack12)",
    ),
    redis: RedisGTRClient = None,
):
    """
    Get rack alerts for a specific rack.

    Equivalent to Flask /api/alert/rack/<rack_number>

    Returns:
    - Battery alerts (1-21): 3 levels each (保護/告警/預警/正常)
    - BAMS alerts (64-80): 2 levels each (異常/正常)
    """
    # In production, fetch from Redis using pattern like f"{rack_number}_alert"
    # For now, return empty/normal status

    battery_alerts: dict[str, str] = {}
    for i in range(1, 22):
        # Each battery alert has 3 levels
        battery_alerts[f"battery_{i}_protection"] = "正常"
        battery_alerts[f"battery_{i}_alarm"] = "正常"
        battery_alerts[f"battery_{i}_warning"] = "正常"

    bams_alerts: dict[str, str] = {}
    for i in range(64, 81):
        # BAMS alerts have 2 levels
        bams_alerts[f"bams_{i}_status"] = "正常"

    return RackAlertResponse(
        rack_number=rack_number,
        battery_alerts=battery_alerts,
        bams_alerts=bams_alerts,
    )
