"""Meter schemas for power monitoring."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MeterData(BaseModel):
    """Individual meter reading data."""

    model_config = ConfigDict(from_attributes=True)

    # Current (per phase)
    I_a: float | None = Field(None, description="Phase A current (A)")
    I_b: float | None = Field(None, description="Phase B current (A)")
    I_c: float | None = Field(None, description="Phase C current (A)")
    I_avg: float | None = Field(None, description="Average current (A)")

    # Voltage (line-to-line)
    Vll_ab: float | None = Field(None, description="Line voltage AB (V)")
    Vll_bc: float | None = Field(None, description="Line voltage BC (V)")
    Vll_ca: float | None = Field(None, description="Line voltage CA (V)")
    Vll_avg: float | None = Field(None, description="Average line voltage (V)")

    # Power
    KW_tot: float | None = Field(None, description="Total active power (kW)")
    KVAR_tot: float | None = Field(None, description="Total reactive power (kVAR)")
    KVA_tot: float | None = Field(None, description="Total apparent power (kVA)")

    # Other
    Freq: float | None = Field(None, description="Frequency (Hz)")
    PF_avg: float | None = Field(None, description="Average power factor")

    # Timestamps
    EventTime: datetime | None = None


class MeterInfoResponse(BaseModel):
    """Meter info response matching Flask /api/meter_info."""

    meters: list[MeterData] = Field(default_factory=list)
    meter_count: int = 0
    total_power: float = 0.0
    status: str = "success"


class AuxMeterData(BaseModel):
    """Auxiliary meter data."""

    model_config = ConfigDict(from_attributes=True)

    EventTime: datetime | None = None
    KW_tot: float | None = Field(None, description="Total active power (kW)")
    KWH_del: float | None = Field(None, description="Energy delivered (kWh)")


class AuxMeterChartData(BaseModel):
    """Auxiliary meter chart data point."""

    timestamp: datetime
    power: float


class AuxMeterSummary(BaseModel):
    """Auxiliary meter summary data."""

    total_energy: float = Field(..., description="Total energy (kWh)")
    avg_power: float = Field(..., description="Average power (kW)")
    max_power: float = Field(..., description="Maximum power (kW)")
    min_power: float = Field(..., description="Minimum power (kW)")


class AuxMeterResponse(BaseModel):
    """Auxiliary meter response matching Flask /api/aux_meter."""

    data: list[AuxMeterChartData] | AuxMeterSummary | None = None
    data_type: str = Field(..., description="chart or summary")
    status: str = "success"
