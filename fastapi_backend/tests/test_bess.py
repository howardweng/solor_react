"""BESS endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_get_bess_info(client: AsyncClient):
    """Test BESS info endpoint returns correct structure."""
    response = await client.get("/api/v1/bess/1")
    data = check_response_or_skip(response)

    assert data["bess_number"] == 1
    assert "table_head" in data
    assert "data" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_bess_info_all_valid_numbers(client: AsyncClient):
    """Test BESS info for all valid numbers 1-12."""
    for bess_num in range(1, 13):
        response = await client.get(f"/api/v1/bess/{bess_num}")
        data = check_response_or_skip(response)

        assert data["bess_number"] == bess_num
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_bess_info_invalid_zero(client: AsyncClient):
    """Test BESS info with invalid number 0."""
    response = await client.get("/api/v1/bess/0")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_bess_info_invalid_too_high(client: AsyncClient):
    """Test BESS info with invalid number > 12."""
    response = await client.get("/api/v1/bess/13")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_bess_info_invalid_negative(client: AsyncClient):
    """Test BESS info with negative number."""
    response = await client.get("/api/v1/bess/-1")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_bess_info_data_structure(client: AsyncClient):
    """Test BESS info data has correct structure."""
    response = await client.get("/api/v1/bess/1")
    data = check_response_or_skip(response)

    # table_head should be a list of rack identifiers
    assert isinstance(data["table_head"], list)

    # data should be a list of metric rows
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        row = data["data"][0]
        assert "metric" in row


@pytest.mark.asyncio
async def test_get_rack_alert(client: AsyncClient):
    """Test rack alert endpoint returns correct structure."""
    response = await client.get("/api/v1/bess/alert/rack/rack01")
    data = check_response_or_skip(response)

    assert data["rack_number"] == "rack01"
    assert "battery_alerts" in data
    assert "bams_alerts" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_rack_alert_all_valid_racks(client: AsyncClient):
    """Test rack alert for all valid rack numbers."""
    for i in range(1, 13):
        rack_num = f"rack{i:02d}"
        response = await client.get(f"/api/v1/bess/alert/rack/{rack_num}")
        data = check_response_or_skip(response)

        assert data["rack_number"] == rack_num
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_rack_alert_invalid_rack00(client: AsyncClient):
    """Test rack alert with invalid rack00."""
    response = await client.get("/api/v1/bess/alert/rack/rack00")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_rack_alert_invalid_rack13(client: AsyncClient):
    """Test rack alert with invalid rack13."""
    response = await client.get("/api/v1/bess/alert/rack/rack13")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_rack_alert_invalid_format(client: AsyncClient):
    """Test rack alert with invalid format."""
    response = await client.get("/api/v1/bess/alert/rack/invalid")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_rack_alert_alerts_structure(client: AsyncClient):
    """Test rack alert response has correct alert structure."""
    response = await client.get("/api/v1/bess/alert/rack/rack01")
    data = check_response_or_skip(response)

    # battery_alerts should be a dict
    assert isinstance(data["battery_alerts"], dict)

    # bams_alerts should be a dict
    assert isinstance(data["bams_alerts"], dict)
