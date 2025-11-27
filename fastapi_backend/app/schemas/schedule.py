"""Schedule schemas for energy trading."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ScheduleEvent(BaseModel):
    """Schedule event data."""

    model_config = ConfigDict(from_attributes=True)

    index: int
    mode: str = Field(..., description="Event mode: dreg, edreg, test_mode, step, scan, full_power")
    time_number: int = Field(..., ge=0, le=23, description="Hour slot 0-23")
    time_start: datetime | None = None
    time_end: datetime | None = None
    time_date: datetime | None = None
    is_get: bool = Field(False, description="Whether bid was won")
    interrupt: bool = Field(False, description="Whether event was interrupted")
    quote_capacity: float | None = Field(None, description="Quoted capacity (kW)")
    power: float | None = Field(None, description="Power (kW)")
    price: float | None = Field(None, description="Actual price")
    quote_price: float | None = Field(None, description="Quoted price")
    quote_code: str | None = None
    title: str | None = None
    description: str | None = None


class ScheduleResponse(BaseModel):
    """Schedule response matching Flask /api/schedule."""

    events: list[ScheduleEvent] = Field(default_factory=list)
    mode: str = Field(..., description="Filter mode applied")
    weeks: int = Field(..., ge=1, le=52, description="Number of weeks")
    total_count: int = 0
    status: str = "success"
