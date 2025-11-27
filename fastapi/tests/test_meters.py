"""Meter endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_meter_info(client: AsyncClient):
    """Test meter info endpoint."""
    response = await client.get("/api/v1/meters")
    assert response.status_code == 200
    data = response.json()
    assert "meters" in data
    assert "meter_count" in data
    assert "total_power" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_aux_meter_chart(client: AsyncClient):
    """Test auxiliary meter endpoint with chart data type."""
    response = await client.get("/api/v1/meters/aux?data_type=chart")
    assert response.status_code == 200
    data = response.json()
    assert data["data_type"] == "chart"
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_aux_meter_summary(client: AsyncClient):
    """Test auxiliary meter endpoint with summary data type."""
    response = await client.get("/api/v1/meters/aux?data_type=summary")
    assert response.status_code == 200
    data = response.json()
    assert data["data_type"] == "summary"
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_aux_meter_invalid_type(client: AsyncClient):
    """Test auxiliary meter with invalid data type."""
    response = await client.get("/api/v1/meters/aux?data_type=invalid")
    assert response.status_code == 422
