"""Schedule and income endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_get_schedule(client: AsyncClient):
    """Test schedule endpoint returns correct structure."""
    response = await client.get("/api/v1/schedule")
    data = check_response_or_skip(response)

    assert "events" in data
    assert "mode" in data
    assert "weeks" in data
    assert "total_count" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_schedule_default_params(client: AsyncClient):
    """Test schedule defaults to all mode and 1 week."""
    response = await client.get("/api/v1/schedule")
    data = check_response_or_skip(response)

    assert data["mode"] == "all"
    assert data["weeks"] == 1


@pytest.mark.asyncio
async def test_get_schedule_with_mode_filter(client: AsyncClient):
    """Test schedule with mode filter."""
    modes = ["all", "dreg", "edreg", "test_mode", "step", "scan", "full_power"]
    for mode in modes:
        response = await client.get(f"/api/v1/schedule?mode={mode}")
        data = check_response_or_skip(response)
        assert data["mode"] == mode


@pytest.mark.asyncio
async def test_get_schedule_with_weeks(client: AsyncClient):
    """Test schedule with weeks parameter."""
    for weeks in [1, 4, 12, 52]:
        response = await client.get(f"/api/v1/schedule?weeks={weeks}")
        data = check_response_or_skip(response)
        assert data["weeks"] == weeks


@pytest.mark.asyncio
async def test_get_schedule_weeks_validation(client: AsyncClient):
    """Test schedule weeks validation (1-52)."""
    # Invalid: 0
    response = await client.get("/api/v1/schedule?weeks=0")
    check_response_or_skip_multi(response, [422])

    # Invalid: 53
    response = await client.get("/api/v1/schedule?weeks=53")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_daily_income(client: AsyncClient):
    """Test daily income endpoint returns correct structure."""
    response = await client.get("/api/v1/schedule/income/daily")
    data = check_response_or_skip(response)

    assert "date" in data
    assert "hourly_data" in data
    assert "total_capacity_fee" in data
    assert "total_efficiency_fee" in data
    assert "total_income" in data
    assert "avg_exec_rate" in data
    assert "avg_performance_index" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_daily_income_with_time(client: AsyncClient):
    """Test daily income with start_time parameter."""
    response = await client.get(
        "/api/v1/schedule/income/daily?start_time=2024-01-15T00:00:00"
    )
    data = check_response_or_skip(response)
    assert data["date"] == "2024-01-15"


@pytest.mark.asyncio
async def test_get_monthly_income(client: AsyncClient):
    """Test monthly income endpoint returns correct structure."""
    response = await client.get("/api/v1/schedule/income/monthly?start_time=2024-01")
    data = check_response_or_skip(response)

    assert "year" in data
    assert "month" in data
    assert "daily_data" in data
    assert "total_capacity_fee" in data
    assert "total_efficiency_fee" in data
    assert "total_income" in data
    assert "avg_exec_rate" in data
    assert "days_with_data" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_monthly_income_validation(client: AsyncClient):
    """Test monthly income requires start_time parameter."""
    response = await client.get("/api/v1/schedule/income/monthly")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_monthly_income_invalid_format(client: AsyncClient):
    """Test monthly income with invalid format."""
    response = await client.get("/api/v1/schedule/income/monthly?start_time=invalid")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_exec_rate(client: AsyncClient):
    """Test exec rate endpoint returns correct structure."""
    response = await client.get(
        "/api/v1/schedule/exec-rate?date=2024-01-15T00:00:00&data_type=exec_rate"
    )
    data = check_response_or_skip(response)

    assert "date" in data
    assert "data_type" in data
    assert "data" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_exec_rate_types(client: AsyncClient):
    """Test exec rate with different data types."""
    types = ["exec_rate", "roll_exec_rate", "hour_exec_rate"]
    for data_type in types:
        response = await client.get(
            f"/api/v1/schedule/exec-rate?date=2024-01-15T00:00:00&data_type={data_type}"
        )
        data = check_response_or_skip(response)
        assert data["data_type"] == data_type


@pytest.mark.asyncio
async def test_get_exec_rate_requires_date(client: AsyncClient):
    """Test exec rate requires date parameter."""
    response = await client.get("/api/v1/schedule/exec-rate")
    check_response_or_skip_multi(response, [422])
