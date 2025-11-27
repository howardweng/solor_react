"""BESS (Battery Energy Storage System) schemas."""
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RackData(BaseModel):
    """Individual rack data in BESS."""

    rack_id: str
    mode: str | None = None
    voltage: float | None = Field(None, description="Voltage in V")
    current: float | None = Field(None, description="Current in A")
    power: float | None = Field(None, description="Power in kW")
    temperature: float | None = Field(None, description="Temperature in °C")
    soc: float | None = Field(None, description="State of Charge %")
    soh: float | None = Field(None, description="State of Health %")
    max_cell_voltage: float | None = None
    min_cell_voltage: float | None = None
    max_cell_temperature: float | None = None
    min_cell_temperature: float | None = None
    cell_voltage_diff: float | None = None
    cell_temperature_diff: float | None = None


class BessInfoResponse(BaseModel):
    """BESS info response matching Flask /api/bams_info/<bess_number>."""

    model_config = ConfigDict(from_attributes=True)

    bess_number: int
    table_head: list[str] = Field(
        default_factory=list,
        description="Table column headers (rack IDs)",
    )
    data: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Table rows with metrics",
    )
    status: str = "success"


class BatteryAlert(BaseModel):
    """Battery alert status."""

    alert_id: int
    level: str = Field(..., description="Alert level: 保護, 告警, 預警, 正常")
    description: str | None = None


class BamsAlert(BaseModel):
    """BAMS (Battery Management System) alert status."""

    alert_id: int
    level: str = Field(..., description="Alert level: 異常, 正常")
    description: str | None = None


class RackAlertResponse(BaseModel):
    """Rack alert response matching Flask /api/alert/rack/<rack_number>."""

    rack_number: str = Field(..., description="Rack identifier (e.g., rack01)")
    battery_alerts: dict[str, str] = Field(
        default_factory=dict,
        description="Battery alerts 1-21 with 3 levels each",
    )
    bams_alerts: dict[str, str] = Field(
        default_factory=dict,
        description="BAMS alerts 64-80 with 2 levels each",
    )
    status: str = "success"
