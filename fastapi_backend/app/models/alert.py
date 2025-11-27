"""Alert models for monitoring and notifications."""
from datetime import datetime, time

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AlertLog(Base):
    """Alert log model for system alerts and notifications."""

    __tablename__ = "alert_log"

    No: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    insert_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    alert_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notify_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    solved_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    hostname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    slaveID: Mapped[str | None] = mapped_column(String(50), nullable=True)
    register: Mapped[str | None] = mapped_column(String(50), nullable=True)
    condition: Mapped[str | None] = mapped_column(String(100), nullable=True)
    value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Alert level: prediction, warning, protection, fault",
    )
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device: Mapped[str | None] = mapped_column(String(100), nullable=True)
    set_pcs_to_zero: Mapped[str | None] = mapped_column(String(10), nullable=True)
    solved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class TimeNumberMap(Base):
    """Time number mapping for hour slots."""

    __tablename__ = "time_number_map"

    number: Mapped[int] = mapped_column(Integer, primary_key=True)
    time_start: Mapped[time | None] = mapped_column(Time, nullable=True)
    time_end: Mapped[time | None] = mapped_column(Time, nullable=True)
