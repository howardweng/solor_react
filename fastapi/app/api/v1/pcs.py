"""PCS (Power Conversion System) endpoints."""
from fastapi import APIRouter, Path

from app.api.deps import RedisGTRClient, PcsSession
from app.models.pcs import int_to_binary_string
from app.schemas.pcs import PcsInfoResponse, PcsAlertResponse

router = APIRouter()


# NOTE: Static routes must be defined before dynamic routes
@router.get("/alert", response_model=PcsAlertResponse)
async def get_pcs_alert(redis: RedisGTRClient = None):
    """
    Get PCS alert status.

    Equivalent to Flask /api/alert/pcs

    Returns 16-bit binary status strings for:
    - inverter_status
    - inverter_inhibits1_status
    - environment_status
    - warning_status
    - grid_status
    - fault_status1, fault_status2
    """
    # In production, fetch from Redis or database
    # For now, return default "all zeros" status

    return PcsAlertResponse(
        inverter_status=int_to_binary_string(0),
        inverter_inhibits1_status=int_to_binary_string(0),
        environment_status=int_to_binary_string(0),
        warning_status=int_to_binary_string(0),
        grid_status=int_to_binary_string(0),
        fault_status1=int_to_binary_string(0),
        fault_status2=int_to_binary_string(0),
    )


@router.get("/{pcs_number}", response_model=PcsInfoResponse)
async def get_pcs_info(
    pcs_number: int = Path(..., ge=1, le=12, description="PCS unit number"),
):
    """
    Get PCS unit information.

    Equivalent to Flask /api/pcs_info/<pcs_number>
    """
    return PcsInfoResponse(pcs_number=pcs_number)
