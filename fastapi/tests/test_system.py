"""System endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_system_overview(client: AsyncClient):
    """Test system overview endpoint."""
    response = await client.get("/api/v1/system/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["segment"] == "system_overview"
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_topology(client: AsyncClient):
    """Test topology endpoint."""
    response = await client.get("/api/v1/system/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "links" in data
    assert "timestamp" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["links"], list)
