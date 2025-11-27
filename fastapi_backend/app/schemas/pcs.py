"""PCS (Power Conversion System) schemas."""
from pydantic import BaseModel, ConfigDict, Field


class PcsInfoResponse(BaseModel):
    """PCS info response matching Flask /api/pcs_info/<pcs_number>."""

    model_config = ConfigDict(from_attributes=True)

    pcs_number: int
    status: str = "success"
    # Add more fields based on actual PCS data structure


class PcsAlertStatus(BaseModel):
    """PCS alert status with 16-bit binary strings."""

    inverter_status: str = Field(
        ...,
        description="Inverter status (16-bit binary)",
        examples=["0000000000000000"],
    )
    inverter_inhibits1_status: str = Field(
        ...,
        description="Inverter inhibits (16-bit binary)",
        examples=["0000000000000000"],
    )
    environment_status: str = Field(
        ...,
        description="Environment status (16-bit binary)",
        examples=["0000000000000000"],
    )
    warning_status: str = Field(
        ...,
        description="Warning status (16-bit binary)",
        examples=["0000000000000000"],
    )
    grid_status: str = Field(
        ...,
        description="Grid status (16-bit binary)",
        examples=["0000000000000000"],
    )
    fault_status1: str = Field(
        ...,
        description="Fault status 1 (16-bit binary)",
        examples=["0000000000000000"],
    )
    fault_status2: str = Field(
        ...,
        description="Fault status 2 (16-bit binary)",
        examples=["0000000000000000"],
    )


class PcsAlertResponse(BaseModel):
    """PCS alert response matching Flask /api/alert/pcs."""

    model_config = ConfigDict(from_attributes=True)

    inverter_status: str = Field(default="0" * 16)
    inverter_inhibits1_status: str = Field(default="0" * 16)
    environment_status: str = Field(default="0" * 16)
    warning_status: str = Field(default="0" * 16)
    grid_status: str = Field(default="0" * 16)
    fault_status1: str = Field(default="0" * 16)
    fault_status2: str = Field(default="0" * 16)
    status: str = "success"
