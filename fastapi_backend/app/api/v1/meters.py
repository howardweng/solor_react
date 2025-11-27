"""Meter endpoints for power monitoring."""
from datetime import date

from fastapi import APIRouter, Query

from app.api.deps import RedisClient, MeterSession
from app.db.redis import redis_scan
from app.schemas.meter import (
    MeterData,
    MeterInfoResponse,
    AuxMeterChartData,
    AuxMeterSummary,
    AuxMeterResponse,
)

router = APIRouter()


@router.get("", response_model=MeterInfoResponse)
async def get_meter_info(redis: RedisClient = None):
    """
    Get all meter data.

    Equivalent to Flask /api/meter_info

    Returns 3-phase meter readings including:
    - Current (A), Voltage (V)
    - Power (kW, kVAR, kVA)
    - Frequency, Power Factor
    """
    meters: list[MeterData] = []
    total_power = 0.0

    # In production, fetch from Redis using pattern "meter_*"
    # Example: data = await redis_scan(redis, "meter_*")

    # For now, return empty data
    return MeterInfoResponse(
        meters=meters,
        meter_count=len(meters),
        total_power=total_power,
    )


@router.get("/aux", response_model=AuxMeterResponse)
async def get_aux_meter(
    time: date = Query(None, description="Date filter (YYYY-MM-DD)"),
    data_type: str = Query(
        "chart",
        description="Response type: chart or summary",
        pattern="^(chart|summary)$",
    ),
    db: MeterSession = None,
):
    """
    Get auxiliary meter data.

    Equivalent to Flask /api/aux_meter

    Args:
        time: Date to filter data
        data_type: "chart" for time-series, "summary" for aggregated stats
    """
    if data_type == "chart":
        # Return time-series data
        chart_data: list[AuxMeterChartData] = []
        # In production, query from database

        return AuxMeterResponse(
            data=chart_data,
            data_type=data_type,
        )
    else:
        # Return summary statistics
        summary = AuxMeterSummary(
            total_energy=0.0,
            avg_power=0.0,
            max_power=0.0,
            min_power=0.0,
        )
        # In production, calculate from database

        return AuxMeterResponse(
            data=summary,
            data_type=data_type,
        )
