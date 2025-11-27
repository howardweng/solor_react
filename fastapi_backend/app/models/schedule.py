"""Schedule event model for energy trading."""
from datetime import datetime, time

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduleEvent(Base):
    """Schedule event model for energy trading bids."""

    __tablename__ = "schedule_events"

    index: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Event mode: dreg, edreg, test_mode, step, scan, full_power",
    )
    time_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Hour slot 0-23",
    )
    quote_capacity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Quoted capacity in kW",
    )
    power: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Power in kW",
    )
    price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Actual price",
    )
    quote_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Quoted price",
    )
    time_start: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Event start time",
    )
    time_end: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Event end time",
    )
    time_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Event date",
    )
    is_get: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether bid was won",
    )
    interrupt: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether event was interrupted",
    )
    quote_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Quote code identifier",
    )
    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Event title",
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Event description",
    )
