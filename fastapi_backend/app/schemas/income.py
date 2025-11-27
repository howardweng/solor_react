"""Income and revenue schemas."""
from datetime import datetime, date

from pydantic import BaseModel, Field


class HourlyIncome(BaseModel):
    """Hourly income breakdown."""

    hour: int = Field(..., ge=0, le=23)
    time_start: datetime | None = None
    time_end: datetime | None = None
    capacity_fee: float = Field(0.0, description="Capacity fee income")
    efficiency_fee: float = Field(0.0, description="Efficiency fee income")
    total: float = Field(0.0, description="Total income")
    exec_rate: float = Field(0.0, description="Execution rate %")
    performance_index: float = Field(0.0, description="Performance index multiplier")


class DailyIncomeResponse(BaseModel):
    """Daily income response matching Flask /api/income/day."""

    date: date
    hourly_data: list[HourlyIncome] = Field(default_factory=list)
    total_capacity_fee: float = 0.0
    total_efficiency_fee: float = 0.0
    total_income: float = 0.0
    avg_exec_rate: float = 0.0
    avg_performance_index: float = 0.0
    status: str = "success"


class DailyIncomeSummary(BaseModel):
    """Daily income summary for monthly report."""

    date: date
    capacity_fee: float = 0.0
    efficiency_fee: float = 0.0
    total: float = 0.0
    exec_rate: float = 0.0


class MonthlyIncomeResponse(BaseModel):
    """Monthly income response matching Flask /api/income/month."""

    year: int
    month: int
    daily_data: list[DailyIncomeSummary] = Field(default_factory=list)
    total_capacity_fee: float = 0.0
    total_efficiency_fee: float = 0.0
    total_income: float = 0.0
    avg_exec_rate: float = 0.0
    days_with_data: int = 0
    status: str = "success"


class ExecRateDataPoint(BaseModel):
    """Execution rate data point."""

    timestamp: datetime
    rate: float = Field(..., ge=0, le=100, description="Execution rate %")


class ExecRateResponse(BaseModel):
    """Execution rate response matching Flask /api/exec_rate."""

    date: date
    data_type: str = Field(..., description="exec_rate, roll_exec_rate, or hour_exec_rate")
    data: list[list] = Field(
        default_factory=list,
        description="[[timestamp, rate], ...] format",
    )
    status: str = "success"
