from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from src.models.doctor import Doctor
from src.models.appointment import Appointment
from src.schemas.doctors import DoctorCreate


def create_doctor(db: Session, payload: DoctorCreate) -> Doctor:
    doctor = Doctor(
        full_name=payload.full_name.strip(),
        specialization=payload.specialization.strip(),
        is_active=True,
    )
    db.add(doctor)
    db.flush()
    db.refresh(doctor)
    return doctor


def get_doctor(db: Session, doctor_id: int) -> Doctor:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    return doctor


def set_doctor_active_status(db: Session, doctor_id: int, is_active: bool) -> Doctor:
    doctor = get_doctor(db, doctor_id)
    doctor.is_active = is_active
    db.add(doctor)
    db.flush()
    db.refresh(doctor)
    return doctor


def delete_doctor(db: Session, doctor_id: int) -> None:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    has_appointments = db.execute(
        select(Appointment.id).where(Appointment.doctor_id == doctor_id).limit(1)
    ).first()

    if has_appointments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctors with existing appointments must not be deleted",
        )

    # Spec prefers deactivation over deletion; we allow deletion only if no appointments exist.
    db.delete(doctor)
    db.flush()
