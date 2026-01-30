from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    Integer,
    DateTime,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.models.base import TimestampMixin


class Appointment(Base, TimestampMixin):
    __tablename__ = "aaryan_singh_appointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("aaryan_singh_patients.id", ondelete="RESTRICT"),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("aaryan_singh_doctors.id", ondelete="RESTRICT"),
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    __table_args__ = (
        Index(
            "idx_doctor_start_time",
            "doctor_id",
            "start_time",
        ),
    )
