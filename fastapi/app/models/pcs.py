"""PCS (Power Conversion System) models."""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PcsData(Base):
    """PCS data model for power conversion system status."""

    __tablename__ = "pcs0_data"

    item: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    EventTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Status registers (stored as integers, converted to 16-bit binary)
    # Register 42632: Inverter status
    inverter_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Inverter status (16-bit)",
    )

    # Register 42651: Inverter inhibits status
    inverter_inhibits1_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Inverter inhibits (16-bit)",
    )

    # Register 42639: Environment status
    environment_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Environment status (16-bit)",
    )

    # Register 42642: Warning status
    warning_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Warning status (16-bit)",
    )

    # Register 42636: Grid status
    grid_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Grid status (16-bit)",
    )

    # Register 42640-42641: Fault status
    fault_status1: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Fault status 1 (16-bit)",
    )
    fault_status2: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Fault status 2 (16-bit)",
    )


def int_to_binary_string(value: int | None, bits: int = 16) -> str:
    """Convert integer to binary string with fixed width."""
    if value is None:
        return "0" * bits
    return format(value & ((1 << bits) - 1), f"0{bits}b")
