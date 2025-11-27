"""Power analysis endpoints."""
from datetime import date, datetime
from typing import Literal

from fastapi import APIRouter, Query

from app.api.deps import MeterSession, BaselineSession
from app.schemas.analysis import (
    PowerLossResponse,
    DailyPowerLoss,
    PowerIOResponse,
    PowerIODataPoint,
    FreqPowerResponse,
)

router = APIRouter()


@router.get("/power-loss", response_model=PowerLossResponse)
async def get_power_loss(
    start_time: datetime = Query(
        ...,
        description="Start time (YYYY-MM-DD HH:MM:SS)",
    ),
    db: MeterSession = None,
):
    """
    Get power loss and efficiency data.

    Equivalent to Flask /api/power_loss

    Returns daily breakdown of:
    - Discharge/charge energy
    - Energy loss and efficiency %
    - Auxiliary power consumption
    """
    target_date = start_time.date()

    # In production, calculate from meter data
    daily_data: list[DailyPowerLoss] = []

    return PowerLossResponse(
        start_date=target_date,
        daily_data=daily_data,
        total_discharge=0.0,
        total_charge=0.0,
        total_loss=0.0,
        avg_efficiency=0.0,
        total_aux=0.0,
    )


@router.get("/power-io", response_model=PowerIOResponse)
async def get_power_io(
    select_time: date = Query(
        ...,
        description="Date (YYYY-MM-DD)",
    ),
    data_type: Literal["daily", "monthly"] = Query(
        "daily",
        description="Data granularity: daily or monthly",
    ),
    db: MeterSession = None,
):
    """
    Get charge/discharge energy data.

    Equivalent to Flask /api/power_io

    Returns time-series of energy flow.
    """
    # In production, query from meter database
    data: list[PowerIODataPoint] = []

    return PowerIOResponse(
        select_date=select_time,
        data_type=data_type,
        data=data,
        total_discharge=0.0,
        total_charge=0.0,
    )


@router.get("/freq-power", response_model=FreqPowerResponse)
async def get_freq_power(
    date_period: int = Query(
        ...,
        description="Period in minutes",
    ),
    select_time: datetime = Query(
        None,
        description="Specific time to query",
    ),
    select_mode: Literal["normalMode", "selectTimeMode"] = Query(
        "normalMode",
        description="Query mode",
    ),
    meter_db: MeterSession = None,
    baseline_db: BaselineSession = None,
):
    """
    Get frequency and power chart data.

    Equivalent to Flask /api/freq_power

    Returns three data series:
    - Frequency data
    - Power data
    - Baseline frequency data
    """
    # In production, query from meter and baseline databases
    # Returns [[timestamp, value], ...] format

    frequency_data: list[list] = []
    power_data: list[list] = []
    baseline_data: list[list] = []

    return FreqPowerResponse(
        date_period=date_period,
        select_time=select_time,
        select_mode=select_mode,
        frequency_data=frequency_data,
        power_data=power_data,
        baseline_data=baseline_data,
    )
