"""System endpoint tests."""
import pytest
from httpx import AsyncClient

from tests.conftest import check_response_or_skip


@pytest.mark.asyncio
async def test_system_overview(client: AsyncClient):
    """Test system overview endpoint returns correct structure."""
    response = await client.get("/api/v1/system/overview")
    data = check_response_or_skip(response)

    assert data["segment"] == "system_overview"
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_topology(client: AsyncClient):
    """Test topology endpoint returns nodes and links."""
    response = await client.get("/api/v1/system/topology")
    data = check_response_or_skip(response)

    # Should have nodes
    assert "nodes" in data
    assert isinstance(data["nodes"], list)

    # Should have links
    assert "links" in data
    assert isinstance(data["links"], list)

    # Should have timestamp
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_topology_nodes_structure(client: AsyncClient):
    """Test topology nodes have correct structure."""
    response = await client.get("/api/v1/system/topology")
    data = check_response_or_skip(response)

    # Check at least some nodes exist (main_server, main_mysql, etc.)
    assert len(data["nodes"]) > 0

    # Each node should have required fields
    for node in data["nodes"]:
        assert "id" in node
        assert "name" in node
        assert "type" in node
        assert "status" in node
        assert node["type"] in ["server", "database", "redis"]
        assert node["status"] in ["online", "offline"]


@pytest.mark.asyncio
async def test_topology_links_structure(client: AsyncClient):
    """Test topology links have correct structure."""
    response = await client.get("/api/v1/system/topology")
    data = check_response_or_skip(response)

    # Each link should have source, target, status
    for link in data["links"]:
        assert "source" in link
        assert "target" in link
        assert "status" in link
        assert link["status"] in ["connected", "disconnected"]
