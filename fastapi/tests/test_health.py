"""Health check endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip, check_response_or_skip_multi


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Test root endpoint returns service info."""
    response = await client.get("/")
    data = check_response_or_skip(response)

    assert data["service"] == "SolarHub API"
    assert data["version"] == "1.0.0"
    assert "docs" in data


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint always returns healthy."""
    response = await client.get("/health")
    data = check_response_or_skip(response)

    assert data["status"] == "healthy"
    assert data["service"] == "SolarHub API"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_health_detailed(client: AsyncClient):
    """Test detailed health check returns infrastructure status."""
    response = await client.get("/health/detailed")
    data = check_response_or_skip(response)

    # Should have status field
    assert "status" in data
    assert data["status"] in ["healthy", "degraded", "unhealthy"]

    # Should have infrastructure details
    assert "infrastructure" in data
    assert "databases" in data["infrastructure"]
    assert "redis" in data["infrastructure"]

    # Database status structure
    db_info = data["infrastructure"]["databases"]
    assert "status" in db_info
    assert "connections" in db_info

    # Redis status structure
    redis_info = data["infrastructure"]["redis"]
    assert "status" in redis_info
    assert "connections" in redis_info

    # Should have a message
    assert "message" in data


@pytest.mark.asyncio
async def test_liveness_check(client: AsyncClient):
    """Test Kubernetes liveness probe."""
    response = await client.get("/health/live")
    data = check_response_or_skip(response)

    assert data["status"] == "alive"


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient):
    """Test Kubernetes readiness probe - may return 503 if no DB."""
    response = await client.get("/health/ready")
    # Can be 200 (ready) or 503 (not ready if no databases)
    # For readiness, 503 is expected behavior, not a skip condition
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    if response.status_code == 200:
        assert data["status"] == "ready"
    else:
        assert data["status"] == "not ready"
        assert "reason" in data
