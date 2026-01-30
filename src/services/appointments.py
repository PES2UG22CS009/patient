from __future__ import annotations

from datetime import datetime, timezone, date, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.appointment import Appointment
from src.models.doctor import Doctor
from src.models.patient import Patient
from src.schemas.appointments import AppointmentCreate


def _ensure_tz_aware(dt: datetime) -> None:
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time must be timezone-aware (include timezone offset)",
        )


def _to_utc(dt: datetime) -> datetime:
    # normalize to UTC for consistent comparisons/storage
    return dt.astimezone(timezone.utc)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def create_appointment(db: Session, payload: AppointmentCreate) -> Appointment:
    # 1) Validate timezone aware (even if schema already checks)
    _ensure_tz_aware(payload.start_time)

    # 2) Validate duration bounds again (service-layer requirement)
    if payload.duration_minutes < 15 or payload.duration_minutes > 180:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="duration_minutes must be between 15 and 180",
        )

    start_utc = _to_utc(payload.start_time)
    end_utc = start_utc + timedelta(minutes=payload.duration_minutes)

    # 3) Reject past appointments
    if start_utc <= _now_utc():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointments must be scheduled in the future",
        )

    # 4) Ensure patient exists
    patient = db.execute(
        select(Patient).where(Patient.id == payload.patient_id)
    ).scalar_one_or_none()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    # 5) Lock doctor row to make scheduling transaction-safe per doctor
    # This ensures two concurrent appointment creations for the same doctor
    # cannot overlap due to race conditions.
    doctor = db.execute(
        select(Doctor).where(Doctor.id == payload.doctor_id).with_for_update()
    ).scalar_one_or_none()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive doctors cannot accept new appointments",
        )

    # 6) Conflict check: overlap if new_start < existing_end AND new_end > existing_start
    # existing_end = existing.start_time + duration_minutes
    # We'll fetch candidates for that doctor and compare in Python (fast enough for clinic scale)
    existing = (
        db.execute(
            select(Appointment).where(Appointment.doctor_id == payload.doctor_id)
        )
        .scalars()
        .all()
    )

    for appt in existing:
        # appt.start_time should be tz-aware; normalize to UTC for comparison
        appt_start = appt.start_time
        if appt_start.tzinfo is None or appt_start.utcoffset() is None:
            # Data integrity fallback
            appt_start = appt_start.replace(tzinfo=timezone.utc)
        appt_start_utc = appt_start.astimezone(timezone.utc)
        appt_end_utc = appt_start_utc + timedelta(minutes=appt.duration_minutes)

        if start_utc < appt_end_utc and end_utc > appt_start_utc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Doctor has a conflicting appointment",
            )

    # 7) Create appointment (store start_time in UTC)
    appointment = Appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        start_time=start_utc,
        duration_minutes=payload.duration_minutes,
    )

    db.add(appointment)
    db.flush()
    db.refresh(appointment)
    return appointment


def list_appointments(
    db: Session, day: date, doctor_id: int | None
) -> list[Appointment]:
    # Interpret the day as UTC day boundaries.
    start_dt = datetime.combine(day, time.min).replace(tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(days=1)

    stmt = select(Appointment).where(
        Appointment.start_time >= start_dt,
        Appointment.start_time < end_dt,
    )

    if doctor_id is not None:
        stmt = stmt.where(Appointment.doctor_id == doctor_id)

    stmt = stmt.order_by(Appointment.start_time.asc())

    return list(db.execute(stmt).scalars().all())
