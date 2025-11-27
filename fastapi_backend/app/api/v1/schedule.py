"""Schedule and income endpoints."""
from datetime import date, datetime, timedelta
from typing import Literal

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.api.deps import ScheduleSession
from app.models.schedule import ScheduleEvent as ScheduleEventModel
from app.schemas.schedule import ScheduleEvent, ScheduleResponse
from app.schemas.income import (
    DailyIncomeResponse,
    MonthlyIncomeResponse,
    ExecRateResponse,
    HourlyIncome,
    DailyIncomeSummary,
)
from app.utils.timezone import utc_to_local

router = APIRouter()


@router.get("", response_model=ScheduleResponse)
async def get_schedule(
    mode: str = Query(
        "all",
        description="Filter by mode: all, dreg, edreg, test_mode, step, scan, full_power",
    ),
    weeks: int = Query(1, ge=1, le=52, description="Number of weeks to fetch"),
    db: ScheduleSession = None,
):
    """
    Get schedule events.

    Equivalent to Flask /api/schedule

    Returns scheduled energy trading events with:
    - Time slots, capacity, power
    - Pricing, bid status
    - Mode and description
    """
    # Build query
    query = select(ScheduleEventModel)

    # Apply mode filter
    if mode != "all":
        query = query.where(ScheduleEventModel.mode == mode)

    # Apply time filter (last N weeks)
    start_date = datetime.now() - timedelta(weeks=weeks)
    query = query.where(ScheduleEventModel.time_date >= start_date)

    # Order by time
    query = query.order_by(ScheduleEventModel.time_date.desc())

    # Execute query
    if db:
        result = await db.execute(query)
        events_db = result.scalars().all()

        events = [
            ScheduleEvent(
                index=e.index,
                mode=e.mode,
                time_number=e.time_number,
                time_start=utc_to_local(e.time_start),
                time_end=utc_to_local(e.time_end),
                time_date=utc_to_local(e.time_date),
                is_get=e.is_get,
                interrupt=e.interrupt,
                quote_capacity=e.quote_capacity,
                power=e.power,
                price=e.price,
                quote_price=e.quote_price,
                quote_code=e.quote_code,
                title=e.title,
                description=e.description,
            )
            for e in events_db
        ]
    else:
        events = []

    return ScheduleResponse(
        events=events,
        mode=mode,
        weeks=weeks,
        total_count=len(events),
    )


@router.get("/income/daily", response_model=DailyIncomeResponse)
async def get_daily_income(
    start_time: datetime = Query(
        None,
        description="Start time (YYYY-MM-DD HH:MM:SS), defaults to today",
    ),
    db: ScheduleSession = None,
):
    """
    Get daily income breakdown.

    Equivalent to Flask /api/income/day

    Returns hourly income with:
    - Capacity and efficiency fees
    - Execution rate
    - Performance index
    """
    target_date = start_time.date() if start_time else date.today()

    # In production, query and calculate from database
    hourly_data: list[HourlyIncome] = []

    return DailyIncomeResponse(
        date=target_date,
        hourly_data=hourly_data,
        total_capacity_fee=0.0,
        total_efficiency_fee=0.0,
        total_income=0.0,
        avg_exec_rate=0.0,
        avg_performance_index=0.0,
    )


@router.get("/income/monthly", response_model=MonthlyIncomeResponse)
async def get_monthly_income(
    start_time: str = Query(
        ...,
        description="Month (YYYY-MM format)",
        pattern=r"^\d{4}-\d{2}$",
    ),
    db: ScheduleSession = None,
):
    """
    Get monthly income summary.

    Equivalent to Flask /api/income/month

    Returns daily totals for the month.
    """
    year, month = map(int, start_time.split("-"))

    # In production, query and calculate from database
    daily_data: list[DailyIncomeSummary] = []

    return MonthlyIncomeResponse(
        year=year,
        month=month,
        daily_data=daily_data,
        total_capacity_fee=0.0,
        total_efficiency_fee=0.0,
        total_income=0.0,
        avg_exec_rate=0.0,
        days_with_data=len(daily_data),
    )


@router.get("/exec-rate", response_model=ExecRateResponse)
async def get_exec_rate(
    date_param: datetime = Query(
        ...,
        alias="date",
        description="Date (YYYY-MM-DD HH:MM:SS)",
    ),
    data_type: Literal["exec_rate", "roll_exec_rate", "hour_exec_rate"] = Query(
        "exec_rate",
        description="Type of execution rate",
    ),
    db: ScheduleSession = None,
):
    """
    Get execution rate time-series.

    Equivalent to Flask /api/exec_rate

    Args:
        date: Target date
        data_type: exec_rate, roll_exec_rate, or hour_exec_rate
    """
    target_date = date_param.date()

    # In production, query from database
    # Returns [[timestamp, rate], ...] format
    data: list[list] = []

    return ExecRateResponse(
        date=target_date,
        data_type=data_type,
        data=data,
    )
