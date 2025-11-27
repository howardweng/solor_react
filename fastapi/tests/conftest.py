"""Pytest fixtures for testing."""
import asyncio
from collections.abc import AsyncGenerator
from typing import Generator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """
    Fixture for authenticated requests.
    In production, this would create a real token.
    """
    return {"Authorization": "Bearer test-token"}


def check_response_or_skip(response, expected_status=200):
    """
    Check response status. Skip test if 503 (DB unavailable).

    Returns the response data if successful.
    Raises pytest.skip if 503.
    Raises AssertionError if other unexpected status.
    """
    if response.status_code == 503:
        pytest.skip(f"Database unavailable (503): {response.json().get('detail', 'No detail')}")

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}: {response.text}"
    )
    return response.json()


def check_response_or_skip_multi(response, expected_statuses):
    """
    Check response against multiple valid statuses. Skip if 503.

    Args:
        response: HTTP response
        expected_statuses: list of valid status codes (e.g., [200, 422])
    """
    if response.status_code == 503:
        pytest.skip(f"Database unavailable (503): {response.json().get('detail', 'No detail')}")

    assert response.status_code in expected_statuses, (
        f"Expected one of {expected_statuses}, got {response.status_code}: {response.text}"
    )
    return response.json() if response.status_code == 200 else None
