"""System overview and topology endpoints."""
from datetime import datetime
import socket

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.system import (
    SystemOverviewResponse,
    TopologyNode,
    TopologyLink,
    TopologyResponse,
)

router = APIRouter()


@router.get("/overview", response_model=SystemOverviewResponse)
async def get_system_overview():
    """
    Get system overview.

    Equivalent to Flask /api/system_overview
    """
    return SystemOverviewResponse(segment="system_overview")


@router.get("/topology", response_model=TopologyResponse)
async def get_topology():
    """
    Get system topology graph.

    Equivalent to Flask /api/topology
    Shows connectivity status of servers, databases, and Redis instances.
    """

    def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
        """Check if a port is reachable."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    nodes = []
    links = []

    # Main server
    main_server_id = "main_server"
    nodes.append(
        TopologyNode(
            id=main_server_id,
            name="Main Server",
            type="server",
            status="online",
            ip=settings.db_host,
        )
    )

    # Main MySQL
    main_mysql_status = "online" if check_port(settings.db_host, settings.db_port) else "offline"
    main_mysql_id = "main_mysql"
    nodes.append(
        TopologyNode(
            id=main_mysql_id,
            name="Main MySQL",
            type="database",
            status=main_mysql_status,
            ip=settings.db_host,
            port=settings.db_port,
        )
    )
    links.append(
        TopologyLink(
            source=main_server_id,
            target=main_mysql_id,
            status="connected" if main_mysql_status == "online" else "disconnected",
        )
    )

    # Main Redis
    main_redis_status = "online" if check_port(settings.redis_host, settings.redis_port) else "offline"
    main_redis_id = "main_redis"
    nodes.append(
        TopologyNode(
            id=main_redis_id,
            name="Main Redis",
            type="redis",
            status=main_redis_status,
            ip=settings.redis_host,
            port=settings.redis_port,
        )
    )
    links.append(
        TopologyLink(
            source=main_server_id,
            target=main_redis_id,
            status="connected" if main_redis_status == "online" else "disconnected",
        )
    )

    # GTR Server
    gtr_server_id = "gtr_server"
    gtr_mysql_status = "online" if check_port(settings.db_host_gtr, settings.db_port) else "offline"
    nodes.append(
        TopologyNode(
            id=gtr_server_id,
            name="GTR Server",
            type="server",
            status="online" if gtr_mysql_status == "online" else "offline",
            ip=settings.db_host_gtr,
        )
    )

    # GTR MySQL
    gtr_mysql_id = "gtr_mysql"
    nodes.append(
        TopologyNode(
            id=gtr_mysql_id,
            name="GTR MySQL",
            type="database",
            status=gtr_mysql_status,
            ip=settings.db_host_gtr,
            port=settings.db_port,
        )
    )
    links.append(
        TopologyLink(
            source=gtr_server_id,
            target=gtr_mysql_id,
            status="connected" if gtr_mysql_status == "online" else "disconnected",
        )
    )

    # GTR Redis
    gtr_redis_status = "online" if check_port(settings.redis_host_gtr, settings.redis_port_gtr) else "offline"
    gtr_redis_id = "gtr_redis"
    nodes.append(
        TopologyNode(
            id=gtr_redis_id,
            name="GTR Redis",
            type="redis",
            status=gtr_redis_status,
            ip=settings.redis_host_gtr,
            port=settings.redis_port_gtr,
        )
    )
    links.append(
        TopologyLink(
            source=gtr_server_id,
            target=gtr_redis_id,
            status="connected" if gtr_redis_status == "online" else "disconnected",
        )
    )

    # Link between main and GTR
    links.append(
        TopologyLink(
            source=main_server_id,
            target=gtr_server_id,
            status="connected" if gtr_mysql_status == "online" else "disconnected",
        )
    )

    return TopologyResponse(
        nodes=nodes,
        links=links,
        timestamp=datetime.now(),
    )
