"""Power analysis schemas."""
from datetime import datetime, date

from pydantic import BaseModel, Field


class DailyPowerLoss(BaseModel):
    """Daily power loss and efficiency data."""

    date: date
    discharge_energy: float = Field(0.0, description="Energy discharged (kWh)")
    charge_energy: float = Field(0.0, description="Energy charged (kWh)")
    loss: float = Field(0.0, description="Energy loss (kWh)")
    efficiency: float = Field(0.0, description="Efficiency %")
    aux_power: float = Field(0.0, description="Auxiliary power consumption (kWh)")
    aux_percentage: float = Field(0.0, description="AUX as % of total")


class PowerLossResponse(BaseModel):
    """Power loss response matching Flask /api/power_loss."""

    start_date: date
    daily_data: list[DailyPowerLoss] = Field(default_factory=list)
    total_discharge: float = 0.0
    total_charge: float = 0.0
    total_loss: float = 0.0
    avg_efficiency: float = 0.0
    total_aux: float = 0.0
    status: str = "success"


class PowerIODataPoint(BaseModel):
    """Power I/O data point."""

    timestamp: datetime | date
    discharge: float = Field(0.0, description="Discharge energy (kWh)")
    charge: float = Field(0.0, description="Charge energy (kWh)")


class PowerIOResponse(BaseModel):
    """Power I/O response matching Flask /api/power_io."""

    select_date: date
    data_type: str = Field(..., description="daily or monthly")
    data: list[PowerIODataPoint] = Field(default_factory=list)
    total_discharge: float = 0.0
    total_charge: float = 0.0
    status: str = "success"


class FreqPowerDataPoint(BaseModel):
    """Frequency and power data point."""

    timestamp: datetime
    frequency: float | None = None
    power: float | None = None
    baseline: float | None = None


class FreqPowerResponse(BaseModel):
    """Frequency and power response matching Flask /api/freq_power."""

    date_period: int = Field(..., description="Period in minutes")
    select_time: datetime | None = None
    select_mode: str = Field(..., description="normalMode or selectTimeMode")
    frequency_data: list[list] = Field(
        default_factory=list,
        description="[[timestamp, frequency], ...]",
    )
    power_data: list[list] = Field(
        default_factory=list,
        description="[[timestamp, power], ...]",
    )
    baseline_data: list[list] = Field(
        default_factory=list,
        description="[[timestamp, baseline], ...]",
    )
    status: str = "success"
