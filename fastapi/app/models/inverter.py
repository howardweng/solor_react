"""Inverter model for solar inverter data."""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Inverter(Base):
    """Inverter model (INVERTER_1) for solar inverter readings."""

    __tablename__ = "INVERTER_1"

    item: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    insert_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    EventTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Power readings
    Nominal_active_power: Mapped[float | None] = mapped_column(Float, nullable=True)
    Total_active_power: Mapped[float | None] = mapped_column(Float, nullable=True)
    Total_apparent_power: Mapped[float | None] = mapped_column(Float, nullable=True)
    Total_reactive_power: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Energy yields
    Daily_power_yields: Mapped[float | None] = mapped_column(Float, nullable=True)
    Total_power_yields: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Status
    Output_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Total_running_time: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    Internal_temperature: Mapped[float | None] = mapped_column(Float, nullable=True)

    # MPPT inputs (1-16)
    MPPT_1_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_1_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_2_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_2_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_3_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_3_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_4_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_4_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_5_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_5_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_6_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_6_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_7_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_7_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_8_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_8_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_9_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_9_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_10_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_10_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_11_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_11_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_12_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_12_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_13_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_13_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_14_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_14_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_15_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_15_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_16_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    MPPT_16_current: Mapped[float | None] = mapped_column(Float, nullable=True)

    # String currents (1-32)
    String_1_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_2_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_3_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_4_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_5_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_6_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_7_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_8_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_9_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_10_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_11_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_12_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_13_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_14_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_15_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_16_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_17_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_18_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_19_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_20_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_21_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_22_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_23_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_24_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_25_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_26_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_27_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_28_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_29_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_30_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_31_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    String_32_current: Mapped[float | None] = mapped_column(Float, nullable=True)

    # AC Phase readings
    Phase_A_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    Phase_A_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    Phase_B_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    Phase_B_current: Mapped[float | None] = mapped_column(Float, nullable=True)
    Phase_C_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    Phase_C_current: Mapped[float | None] = mapped_column(Float, nullable=True)

    # DC readings
    Bus_voltage: Mapped[float | None] = mapped_column(Float, nullable=True)
    DC_power: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Insulation and faults
    Array_insulation_resistance: Mapped[float | None] = mapped_column(Float, nullable=True)
    Device_fault_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
