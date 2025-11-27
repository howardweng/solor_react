"""Inverter endpoints."""
from fastapi import APIRouter

from app.api.deps import RedisClient, InverterSession
from app.schemas.inverter import (
    InverterData,
    InverterResponse,
    MpptData,
    StringCurrent,
    PhaseData,
)

router = APIRouter()


@router.get("", response_model=InverterResponse)
async def get_inverter_data(redis: RedisClient = None):
    """
    Get inverter measurements.

    Equivalent to Flask /api/converter

    Returns:
    - Power readings (active, apparent, reactive)
    - Energy yields (daily, total)
    - MPPT data (1-16)
    - String currents (1-32)
    - AC phase data (A, B, C)
    - DC readings
    """
    # In production, fetch from Redis or database

    inverter_data = InverterData(
        nominal_active_power=None,
        total_active_power=None,
        total_apparent_power=None,
        total_reactive_power=None,
        daily_power_yields=None,
        total_power_yields=None,
        internal_temperature=None,
        bus_voltage=None,
        dc_power=None,
    )

    # MPPT data (1-16)
    mppt_data = [
        MpptData(mppt_id=i, voltage=None, current=None, power=None)
        for i in range(1, 17)
    ]

    # String currents (1-32)
    string_currents = [
        StringCurrent(string_id=i, current=None)
        for i in range(1, 33)
    ]

    # Phase data
    phase_data = [
        PhaseData(phase="A", voltage=None, current=None),
        PhaseData(phase="B", voltage=None, current=None),
        PhaseData(phase="C", voltage=None, current=None),
    ]

    return InverterResponse(
        inverter_data=inverter_data,
        mppt_data=mppt_data,
        string_currents=string_currents,
        phase_data=phase_data,
    )
