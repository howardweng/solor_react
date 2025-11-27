"""Power analysis endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_get_power_loss(client: AsyncClient):
    """Test power loss endpoint returns correct structure."""
    response = await client.get(
        "/api/v1/analysis/power-loss?start_time=2024-01-15T00:00:00"
    )
    data = check_response_or_skip(response)

    assert "start_date" in data
    assert "daily_data" in data
    assert "total_discharge" in data
    assert "total_charge" in data
    assert "total_loss" in data
    assert "avg_efficiency" in data
    assert "total_aux" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_power_loss_requires_start_time(client: AsyncClient):
    """Test power loss requires start_time parameter."""
    response = await client.get("/api/v1/analysis/power-loss")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_power_io(client: AsyncClient):
    """Test power I/O endpoint returns correct structure."""
    response = await client.get("/api/v1/analysis/power-io?select_time=2024-01-15")
    data = check_response_or_skip(response)

    assert "select_date" in data
    assert "data_type" in data
    assert "data" in data
    assert "total_discharge" in data
    assert "total_charge" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_power_io_daily(client: AsyncClient):
    """Test power I/O with daily data type."""
    response = await client.get(
        "/api/v1/analysis/power-io?select_time=2024-01-15&data_type=daily"
    )
    data = check_response_or_skip(response)
    assert data["data_type"] == "daily"


@pytest.mark.asyncio
async def test_get_power_io_monthly(client: AsyncClient):
    """Test power I/O with monthly data type."""
    response = await client.get(
        "/api/v1/analysis/power-io?select_time=2024-01-15&data_type=monthly"
    )
    data = check_response_or_skip(response)
    assert data["data_type"] == "monthly"


@pytest.mark.asyncio
async def test_get_power_io_requires_select_time(client: AsyncClient):
    """Test power I/O requires select_time parameter."""
    response = await client.get("/api/v1/analysis/power-io")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_freq_power(client: AsyncClient):
    """Test frequency power endpoint returns correct structure."""
    response = await client.get("/api/v1/analysis/freq-power?date_period=60")
    data = check_response_or_skip(response)

    assert "date_period" in data
    assert "select_mode" in data
    assert "frequency_data" in data
    assert "power_data" in data
    assert "baseline_data" in data
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_freq_power_requires_date_period(client: AsyncClient):
    """Test freq power requires date_period parameter."""
    response = await client.get("/api/v1/analysis/freq-power")
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_get_freq_power_modes(client: AsyncClient):
    """Test freq power with normal mode."""
    response = await client.get(
        "/api/v1/analysis/freq-power?date_period=60&select_mode=normalMode"
    )
    data = check_response_or_skip(response)
    assert data["select_mode"] == "normalMode"


@pytest.mark.asyncio
async def test_get_freq_power_select_time_mode(client: AsyncClient):
    """Test freq power with select time mode."""
    response = await client.get(
        "/api/v1/analysis/freq-power?date_period=60&select_mode=selectTimeMode&select_time=2024-01-15T12:00:00"
    )
    data = check_response_or_skip(response)
    assert data["select_mode"] == "selectTimeMode"
