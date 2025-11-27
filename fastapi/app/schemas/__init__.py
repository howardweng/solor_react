"""Pydantic schemas for API request/response models."""
from .common import BaseResponse, MessageResponse, StatusResponse
from .auth import (
    LoginRequest,
    TokenResponse,
    UserResponse,
    UserCreate,
    UserUpdate,
)
from .bess import BessInfoResponse, RackAlertResponse
from .pcs import PcsInfoResponse, PcsAlertResponse
from .meter import MeterInfoResponse, MeterData, AuxMeterResponse
from .inverter import InverterResponse
from .schedule import ScheduleResponse, ScheduleEvent
from .income import DailyIncomeResponse, MonthlyIncomeResponse, ExecRateResponse
from .analysis import PowerLossResponse, PowerIOResponse, FreqPowerResponse
from .config import SidebarInfoResponse, HeaderInfoResponse
from .system import SystemOverviewResponse, TopologyResponse

__all__ = [
    # Common
    "BaseResponse",
    "MessageResponse",
    "StatusResponse",
    # Auth
    "LoginRequest",
    "TokenResponse",
    "UserResponse",
    "UserCreate",
    "UserUpdate",
    # BESS
    "BessInfoResponse",
    "RackAlertResponse",
    # PCS
    "PcsInfoResponse",
    "PcsAlertResponse",
    # Meter
    "MeterInfoResponse",
    "MeterData",
    "AuxMeterResponse",
    # Inverter
    "InverterResponse",
    # Schedule
    "ScheduleResponse",
    "ScheduleEvent",
    # Income
    "DailyIncomeResponse",
    "MonthlyIncomeResponse",
    "ExecRateResponse",
    # Analysis
    "PowerLossResponse",
    "PowerIOResponse",
    "FreqPowerResponse",
    # Config
    "SidebarInfoResponse",
    "HeaderInfoResponse",
    # System
    "SystemOverviewResponse",
    "TopologyResponse",
]
