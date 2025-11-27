"""Application configuration using Pydantic Settings."""
from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    secret_key: str = Field(default="change-me-in-production")

    # Main Database
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""

    # Database names
    db_name_ess: str = "ess"
    db_name_schedule: str = "schedule"
    db_name_meter: str = "Meter"
    db_name_pcs: str = "PCS"
    db_name_inverter: str = "Inverter"
    db_name_baseline: str = "BaseLine"

    # BESS databases (1-12)
    db_name_bess1: str = "BESS1"
    db_name_bess2: str = "BESS2"
    db_name_bess3: str = "BESS3"
    db_name_bess4: str = "BESS4"
    db_name_bess5: str = "BESS5"
    db_name_bess6: str = "BESS6"
    db_name_bess7: str = "BESS7"
    db_name_bess8: str = "BESS8"
    db_name_bess9: str = "BESS9"
    db_name_bess10: str = "BESS10"
    db_name_bess11: str = "BESS11"
    db_name_bess12: str = "BESS12"

    # GTR Database
    db_host_gtr: str = "192.168.10.46"
    db_user_gtr: str = "root"
    db_password_gtr: str = ""

    # Redis - Main
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    # Redis - GTR
    redis_host_gtr: str = "192.168.10.46"
    redis_port_gtr: int = 6379
    redis_password_gtr: str = ""

    # System Configuration
    bess_number: int = 2
    pcs_number: int = 2
    rack_number: int = 12
    inverter_number: int = 2
    bess_type: str = "BESS"
    pcs_type: str = "PCS"

    # Energy Trading
    quote_code: str = ""
    qse_id: str = ""
    resource_id: str = ""
    reg_type: str = ""

    # External Services
    cctv_url: str = ""
    tcp_host: str = ""
    tcp_port: int = 0

    # LINE Notifications
    line_notify_token: str = ""
    lotify_client_id: str = ""
    lotify_client_secret: str = ""

    # JWT Settings
    jwt_secret_key: str = Field(default="jwt-secret-change-me")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Computed database URLs
    @computed_field
    @property
    def database_url_ess(self) -> str:
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name_ess}"

    @computed_field
    @property
    def database_url_schedule(self) -> str:
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name_schedule}"

    @computed_field
    @property
    def database_url_meter(self) -> str:
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name_meter}"

    @computed_field
    @property
    def database_url_pcs(self) -> str:
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name_pcs}"

    @computed_field
    @property
    def database_url_inverter(self) -> str:
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name_inverter}"

    @computed_field
    @property
    def database_url_baseline(self) -> str:
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name_baseline}"

    def get_bess_database_url(self, bess_number: int) -> str:
        """Get database URL for a specific BESS unit."""
        db_name = getattr(self, f"db_name_bess{bess_number}", f"BESS{bess_number}")
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{db_name}"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()
