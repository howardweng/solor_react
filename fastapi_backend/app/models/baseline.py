"""Baseline model for frequency baseline data."""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BaseLine(Base):
    """Baseline frequency model."""

    __tablename__ = "base_line"

    item: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    insert_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    baseline_freq: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Baseline frequency in Hz",
    )
