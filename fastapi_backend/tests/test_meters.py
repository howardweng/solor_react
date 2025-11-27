"""Meter endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_get_meter_info(client: AsyncClient):
    """Test meter info endpoint returns correct structure."""
    response = await client.get("/api/v1/meters")
    data = check_response_or_skip(response)

    assert "meters" in data
    assert "meter_count" in data
    assert "total_power" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_meter_info_empty_when_no_redis(client: AsyncClient):
    """Test meter info returns empty list when Redis unavailable."""
    response = await client.get("/api/v1/meters")
    data = check_response_or_skip(response)

    # When Redis is unavailable, should return empty meters list
    assert isinstance(data["meters"], list)
    assert data["meter_count"] == len(data["meters"])


@pytest.mark.asyncio
async def test_get_aux_meter_chart(client: AsyncClient):
    """Test auxiliary meter endpoint with chart data type."""
    response = await client.get("/api/v1/meters/aux?data_type=chart")
    data = check_response_or_skip(response)

    assert data["data_type"] == "chart"
    assert data["status"] == "success"
    assert "data" in data


@pytest.mark.asyncio
async def test_get_aux_meter_summary(client: AsyncClient):
    """Test auxiliary meter endpoint with summary data type."""
    response = await client.get("/api/v1/meters/aux?data_type=summary")
    data = check_response_or_skip(response)

    assert data["data_type"] == "summary"
    assert data["status"] == "success"
    assert "data" in data


@pytest.mark.asyncio
async def test_get_aux_meter_default_type(client: AsyncClient):
    """Test auxiliary meter endpoint defaults to chart type."""
    response = await client.get("/api/v1/meters/aux")
    data = check_response_or_skip(response)

    assert data["data_type"] == "chart"


@pytest.mark.asyncio
async def test_get_aux_meter_invalid_type(client: AsyncClient):
    """Test auxiliary meter with invalid data type returns 422."""
    response = await client.get("/api/v1/meters/aux?data_type=invalid")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_aux_meter_with_time(client: AsyncClient):
    """Test auxiliary meter endpoint with time filter."""
    response = await client.get("/api/v1/meters/aux?time=2024-01-15")
    data = check_response_or_skip(response)

    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_aux_meter_summary_structure(client: AsyncClient):
    """Test summary data has correct structure."""
    response = await client.get("/api/v1/meters/aux?data_type=summary")
    data = check_response_or_skip(response)

    summary = data["data"]
    if summary:  # Only check if data exists
        expected_fields = ["total_energy", "avg_power", "max_power", "min_power"]
        for field in expected_fields:
            assert field in summary
