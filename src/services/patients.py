from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status

from src.models.patient import Patient
from src.models.appointment import Appointment
from src.schemas.patients import PatientCreate


def create_patient(db: Session, payload: PatientCreate) -> Patient:
    # Service-level uniqueness check (fast fail)
    existing = db.query(Patient).filter(Patient.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    patient = Patient(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=str(payload.email).lower(),
        phone=payload.phone.strip(),
    )

    db.add(patient)

    try:
        # Force insert now so we can return ID and catch unique constraint
        db.flush()
    except IntegrityError:
        # If race condition occurred (two requests same email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    db.refresh(patient)
    return patient


def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient


def delete_patient(db: Session, patient_id: int) -> None:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    has_appointments = db.execute(
        select(Appointment.id).where(Appointment.patient_id == patient_id).limit(1)
    ).first()

    if has_appointments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patients with existing appointments must not be deleted",
        )

    db.delete(patient)
    db.flush()
