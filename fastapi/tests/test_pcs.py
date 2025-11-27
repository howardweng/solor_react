"""PCS endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_get_pcs_info(client: AsyncClient):
    """Test PCS info endpoint returns correct structure."""
    response = await client.get("/api/v1/pcs/1")
    data = check_response_or_skip(response)

    assert data["pcs_number"] == 1
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_pcs_info_all_valid_numbers(client: AsyncClient):
    """Test PCS info for all valid numbers 1-12."""
    for pcs_num in range(1, 13):
        response = await client.get(f"/api/v1/pcs/{pcs_num}")
        data = check_response_or_skip(response)

        assert data["pcs_number"] == pcs_num
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_pcs_info_invalid_zero(client: AsyncClient):
    """Test PCS info with invalid number 0."""
    response = await client.get("/api/v1/pcs/0")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_pcs_info_invalid_too_high(client: AsyncClient):
    """Test PCS info with invalid number > 12."""
    response = await client.get("/api/v1/pcs/13")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_pcs_alert(client: AsyncClient):
    """Test PCS alert endpoint returns binary status strings."""
    response = await client.get("/api/v1/pcs/alert")
    data = check_response_or_skip(response)

    # Check all status fields are 16-bit binary strings
    status_fields = [
        "inverter_status",
        "inverter_inhibits1_status",
        "environment_status",
        "warning_status",
        "grid_status",
        "fault_status1",
        "fault_status2",
    ]

    for field in status_fields:
        assert field in data
        assert len(data[field]) == 16
        assert all(c in "01" for c in data[field])

    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_pcs_alert_default_status(client: AsyncClient):
    """Test PCS alert returns default (all zeros) when no data."""
    response = await client.get("/api/v1/pcs/alert")
    data = check_response_or_skip(response)

    # Default should be all zeros (no alerts)
    assert data["inverter_status"] == "0000000000000000"
