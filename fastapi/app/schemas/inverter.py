"""Inverter schemas for solar inverter data."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MpptData(BaseModel):
    """MPPT (Maximum Power Point Tracking) input data."""

    mppt_id: int
    voltage: float | None = Field(None, description="Voltage (V)")
    current: float | None = Field(None, description="Current (A)")
    power: float | None = Field(None, description="Power (W)")


class StringCurrent(BaseModel):
    """String current data."""

    string_id: int
    current: float | None = Field(None, description="Current (A)")


class PhaseData(BaseModel):
    """AC phase data."""

    phase: str = Field(..., description="Phase identifier (A, B, C)")
    voltage: float | None = Field(None, description="Voltage (V)")
    current: float | None = Field(None, description="Current (A)")


class InverterData(BaseModel):
    """Inverter measurement data."""

    model_config = ConfigDict(from_attributes=True)

    # Power readings
    nominal_active_power: float | None = Field(None, description="Nominal active power (kW)")
    total_active_power: float | None = Field(None, description="Total active power (kW)")
    total_apparent_power: float | None = Field(None, description="Total apparent power (kVA)")
    total_reactive_power: float | None = Field(None, description="Total reactive power (kVAR)")

    # Energy yields
    daily_power_yields: float | None = Field(None, description="Daily energy yield (kWh)")
    total_power_yields: float | None = Field(None, description="Total energy yield (kWh)")

    # Status
    output_type: int | None = None
    total_running_time: int | None = Field(None, description="Total running time (seconds)")
    internal_temperature: float | None = Field(None, description="Internal temperature (°C)")

    # DC readings
    bus_voltage: float | None = Field(None, description="DC bus voltage (V)")
    dc_power: float | None = Field(None, description="DC power (kW)")

    # Other
    array_insulation_resistance: float | None = Field(None, description="Insulation resistance (kΩ)")
    device_fault_code: int | None = None

    # Timestamps
    event_time: datetime | None = None


class InverterResponse(BaseModel):
    """Inverter response matching Flask /api/converter."""

    # Main data
    inverter_data: InverterData | None = None

    # MPPT data (1-16)
    mppt_data: list[MpptData] = Field(default_factory=list)

    # String currents (1-32)
    string_currents: list[StringCurrent] = Field(default_factory=list)

    # Phase data (A, B, C)
    phase_data: list[PhaseData] = Field(default_factory=list)

    status: str = "success"
