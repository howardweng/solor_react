"""Configuration endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_sidebar_info(client: AsyncClient):
    """Test sidebar info endpoint."""
    response = await client.get("/api/v1/config/sidebar")
    assert response.status_code == 200
    data = response.json()
    assert "bess_type" in data
    assert "bess_number" in data
    assert "pcs_number" in data
    assert "inverter_number" in data
    assert "rack_number" in data
    assert "number_of_devices" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_header_info(client: AsyncClient):
    """Test header info endpoint."""
    response = await client.get("/api/v1/config/header")
    assert response.status_code == 200
    data = response.json()
    assert "protection_info" in data
    assert "warning_info" in data
    assert "fault_info" in data
    assert data["status"] == "success"
