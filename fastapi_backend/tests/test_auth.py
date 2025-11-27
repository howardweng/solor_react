"""Authentication endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip_multi


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials returns 401 or 503 (if DB unavailable)."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "invalid", "password": "invalid"},
    )
    # 401 if DB available but credentials wrong
    # Skip if 503 (DB unavailable)
    check_response_or_skip_multi(response, [401])


@pytest.mark.asyncio
async def test_login_json_invalid_credentials(client: AsyncClient):
    """Test JSON login with invalid credentials."""
    response = await client.post(
        "/api/v1/auth/login/json",
        json={"username": "invalid", "password": "invalid"},
    )
    check_response_or_skip_multi(response, [401])


@pytest.mark.asyncio
async def test_login_missing_fields(client: AsyncClient):
    """Test login with missing fields returns 422."""
    response = await client.post(
        "/api/v1/auth/login",
        data={},
    )
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_login_json_missing_fields(client: AsyncClient):
    """Test JSON login with missing fields returns 422."""
    response = await client.post(
        "/api/v1/auth/login/json",
        json={},
    )
    check_response_or_skip_multi(response, [422])


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    """Test refresh with invalid token returns 401."""
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid-token"},
    )
    check_response_or_skip_multi(response, [401])


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client: AsyncClient):
    """Test /me endpoint without auth returns 401."""
    response = await client.get("/api/v1/auth/me")
    check_response_or_skip_multi(response, [401])


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """Test /me endpoint with invalid token returns 401."""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    check_response_or_skip_multi(response, [401])


@pytest.mark.asyncio
async def test_logout_unauthenticated(client: AsyncClient):
    """Test logout without auth returns 401."""
    response = await client.post("/api/v1/auth/logout")
    check_response_or_skip_multi(response, [401])
