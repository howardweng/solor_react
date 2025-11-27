"""System overview and topology schemas."""
from datetime import datetime

from pydantic import BaseModel, Field


class SystemOverviewResponse(BaseModel):
    """System overview response matching Flask /api/system_overview."""

    segment: str = "system_overview"
    status: str = "success"


class TopologyNode(BaseModel):
    """Node in the system topology graph."""

    id: str
    name: str
    type: str = Field(..., description="Node type: server, database, redis, etc.")
    status: str = Field(..., description="Status: online, offline, error")
    ip: str | None = None
    port: int | None = None


class TopologyLink(BaseModel):
    """Link between topology nodes."""

    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    status: str = Field(..., description="Link status: connected, disconnected")


class TopologyResponse(BaseModel):
    """Topology response matching Flask /api/topology."""

    nodes: list[TopologyNode] = Field(default_factory=list)
    links: list[TopologyLink] = Field(default_factory=list)
    timestamp: datetime
    status: str = "success"
