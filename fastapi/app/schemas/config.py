"""Configuration schemas."""
from pydantic import BaseModel, Field


class SidebarInfoResponse(BaseModel):
    """Sidebar info response matching Flask /api/sidebar_info."""

    bess_type: str = Field(..., description="BESS type identifier")
    bess_number: int = Field(..., description="Number of BESS units")
    pcs_number: int = Field(..., description="Number of PCS units")
    inverter_number: int = Field(..., description="Number of inverters")
    rack_number: int = Field(..., description="Number of racks")
    number_of_devices: int = Field(..., description="Total device count")
    cctv_url: str | None = Field(None, description="CCTV stream URL")
    status: str = "success"


class AlertSummary(BaseModel):
    """Alert summary for header."""

    count: int = 0
    items: list[str] = Field(default_factory=list)


class HeaderInfoResponse(BaseModel):
    """Header info response matching Flask /api/header_info."""

    protection_info: AlertSummary = Field(default_factory=AlertSummary)
    warning_info: AlertSummary = Field(default_factory=AlertSummary)
    fault_info: AlertSummary = Field(default_factory=AlertSummary)
    status: str = "success"
