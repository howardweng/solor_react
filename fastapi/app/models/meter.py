"""Meter models for power monitoring."""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MainMeter(Base):
    """Main meter (MMAIN) model for primary power readings."""

    __tablename__ = "MMAIN"

    item: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    EventTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Voltage (line-to-line)
    Vll_ab: Mapped[float | None] = mapped_column(Float, nullable=True)
    Vll_bc: Mapped[float | None] = mapped_column(Float, nullable=True)
    Vll_ca: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Current (per phase)
    I_a: Mapped[float | None] = mapped_column(Float, nullable=True)
    I_b: Mapped[float | None] = mapped_column(Float, nullable=True)
    I_c: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Power
    KW_tot: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Total active power kW")
    KVAR_tot: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Total reactive power kVAR")
    KVA_tot: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Total apparent power kVA")

    # Energy
    KWH_del: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Energy delivered (discharge)")
    KWH_rec: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Energy received (charge)")

    # Other
    Freq: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Frequency Hz")
    PF_avg: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Average power factor")

    # Execution rates (stored as integer * 100)
    SBSPM: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Execution rate")
    roll_SBSPM: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Rolling execution rate")
    hour_SBSPM: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Hourly execution rate")


class AuxMeter(Base):
    """Auxiliary meter (MAUX) model for secondary power readings."""

    __tablename__ = "MAUX"

    item: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    EventTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    KW_tot: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Total active power kW")
    KWH_del: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Energy delivered kWh")
