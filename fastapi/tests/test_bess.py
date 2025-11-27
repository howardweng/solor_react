"""BESS endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_bess_info(client: AsyncClient):
    """Test BESS info endpoint."""
    response = await client.get("/api/v1/bess/1")
    assert response.status_code == 200
    data = response.json()
    assert data["bess_number"] == 1
    assert "table_head" in data
    assert "data" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_bess_info_invalid(client: AsyncClient):
    """Test BESS info with invalid number."""
    response = await client.get("/api/v1/bess/0")
    assert response.status_code == 422  # Validation error

    response = await client.get("/api/v1/bess/13")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_rack_alert(client: AsyncClient):
    """Test rack alert endpoint."""
    response = await client.get("/api/v1/bess/alert/rack/rack01")
    assert response.status_code == 200
    data = response.json()
    assert data["rack_number"] == "rack01"
    assert "battery_alerts" in data
    assert "bams_alerts" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_rack_alert_invalid(client: AsyncClient):
    """Test rack alert with invalid rack number."""
    response = await client.get("/api/v1/bess/alert/rack/rack00")
    assert response.status_code == 422

    response = await client.get("/api/v1/bess/alert/rack/invalid")
    assert response.status_code == 422
