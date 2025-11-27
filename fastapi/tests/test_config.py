"""Configuration endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_sidebar_info(client: AsyncClient):
    """Test sidebar info endpoint returns system configuration."""
    response = await client.get("/api/v1/config/sidebar")
    data = check_response_or_skip(response)

    # Check all required fields
    assert "bess_type" in data
    assert "bess_number" in data
    assert "pcs_number" in data
    assert "inverter_number" in data
    assert "rack_number" in data
    assert "number_of_devices" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_sidebar_info_device_count(client: AsyncClient):
    """Test sidebar info number_of_devices is correct sum."""
    response = await client.get("/api/v1/config/sidebar")
    data = check_response_or_skip(response)

    # number_of_devices should be sum of all device counts
    expected_total = (
        data["bess_number"]
        + data["pcs_number"]
        + data["inverter_number"]
        + data["rack_number"]
    )
    assert data["number_of_devices"] == expected_total


@pytest.mark.asyncio
async def test_sidebar_info_types(client: AsyncClient):
    """Test sidebar info field types are correct."""
    response = await client.get("/api/v1/config/sidebar")
    data = check_response_or_skip(response)

    assert isinstance(data["bess_type"], str)
    assert isinstance(data["bess_number"], int)
    assert isinstance(data["pcs_number"], int)
    assert isinstance(data["inverter_number"], int)
    assert isinstance(data["rack_number"], int)
    assert isinstance(data["number_of_devices"], int)


@pytest.mark.asyncio
async def test_sidebar_info_cctv_url(client: AsyncClient):
    """Test sidebar info may include optional cctv_url."""
    response = await client.get("/api/v1/config/sidebar")
    data = check_response_or_skip(response)

    # cctv_url should be present (can be null or string)
    assert "cctv_url" in data
    assert data["cctv_url"] is None or isinstance(data["cctv_url"], str)


@pytest.mark.asyncio
async def test_header_info(client: AsyncClient):
    """Test header info endpoint returns alert summary."""
    response = await client.get("/api/v1/config/header")
    data = check_response_or_skip(response)

    assert "protection_info" in data
    assert "warning_info" in data
    assert "fault_info" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_header_info_alert_structure(client: AsyncClient):
    """Test header info alert summaries have correct structure."""
    response = await client.get("/api/v1/config/header")
    data = check_response_or_skip(response)

    for alert_type in ["protection_info", "warning_info", "fault_info"]:
        alert_data = data[alert_type]
        assert "count" in alert_data
        assert "items" in alert_data
        assert isinstance(alert_data["count"], int)
        assert isinstance(alert_data["items"], list)


@pytest.mark.asyncio
async def test_header_info_alert_counts(client: AsyncClient):
    """Test header info alert counts are non-negative integers."""
    response = await client.get("/api/v1/config/header")
    data = check_response_or_skip(response)

    for alert_type in ["protection_info", "warning_info", "fault_info"]:
        assert data[alert_type]["count"] >= 0
