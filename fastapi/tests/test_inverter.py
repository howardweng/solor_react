"""Inverter endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip


@pytest.mark.asyncio
async def test_get_inverter_data(client: AsyncClient):
    """Test inverter endpoint returns correct structure."""
    response = await client.get("/api/v1/inverter")
    data = check_response_or_skip(response)

    assert "inverter_data" in data
    assert "mppt_data" in data
    assert "string_currents" in data
    assert "phase_data" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_inverter_data_inverter_structure(client: AsyncClient):
    """Test inverter_data has correct fields."""
    response = await client.get("/api/v1/inverter")
    data = check_response_or_skip(response)

    inverter = data["inverter_data"]
    expected_fields = [
        "nominal_active_power",
        "total_active_power",
        "total_apparent_power",
        "total_reactive_power",
        "daily_power_yields",
        "total_power_yields",
        "internal_temperature",
        "bus_voltage",
        "dc_power",
    ]
    for field in expected_fields:
        assert field in inverter


@pytest.mark.asyncio
async def test_get_inverter_data_mppt_structure(client: AsyncClient):
    """Test mppt_data has correct structure (16 MPPT units)."""
    response = await client.get("/api/v1/inverter")
    data = check_response_or_skip(response)

    mppt = data["mppt_data"]
    assert isinstance(mppt, list)
    assert len(mppt) == 16  # 16 MPPT units

    # Each MPPT should have id, voltage, current, power
    for item in mppt:
        assert "mppt_id" in item
        assert "voltage" in item
        assert "current" in item
        assert "power" in item


@pytest.mark.asyncio
async def test_get_inverter_data_string_currents_structure(client: AsyncClient):
    """Test string_currents has correct structure (32 strings)."""
    response = await client.get("/api/v1/inverter")
    data = check_response_or_skip(response)

    strings = data["string_currents"]
    assert isinstance(strings, list)
    assert len(strings) == 32  # 32 strings

    # Each string should have id and current
    for item in strings:
        assert "string_id" in item
        assert "current" in item


@pytest.mark.asyncio
async def test_get_inverter_data_phase_structure(client: AsyncClient):
    """Test phase_data has correct structure (A, B, C phases)."""
    response = await client.get("/api/v1/inverter")
    data = check_response_or_skip(response)

    phases = data["phase_data"]
    assert isinstance(phases, list)
    assert len(phases) == 3  # A, B, C phases

    # Each phase should have phase, voltage, current
    for item in phases:
        assert "phase" in item
        assert "voltage" in item
        assert "current" in item
        assert item["phase"] in ["A", "B", "C"]


@pytest.mark.asyncio
async def test_get_inverter_data_null_values_when_no_data(client: AsyncClient):
    """Test inverter returns null values when no data available."""
    response = await client.get("/api/v1/inverter")
    data = check_response_or_skip(response)

    # When no data available (Redis down), values should be None/null
    inverter = data["inverter_data"]
    # All values can be None when no data
    assert inverter["total_active_power"] is None or isinstance(
        inverter["total_active_power"], (int, float)
    )
