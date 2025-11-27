"""PCS endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_pcs_info(client: AsyncClient):
    """Test PCS info endpoint."""
    response = await client.get("/api/v1/pcs/1")
    assert response.status_code == 200
    data = response.json()
    assert data["pcs_number"] == 1
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_pcs_alert(client: AsyncClient):
    """Test PCS alert endpoint."""
    response = await client.get("/api/v1/pcs/alert")
    assert response.status_code == 200
    data = response.json()

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
