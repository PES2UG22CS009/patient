from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.doctors import DoctorCreate, DoctorRead
from src.services import doctors as doctors_service

router = APIRouter()


@router.post("", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    return doctors_service.create_doctor(db, payload)


@router.get("/{doctor_id}", response_model=DoctorRead, status_code=status.HTTP_200_OK)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctors_service.get_doctor(db, doctor_id)


@router.patch(
    "/{doctor_id}/deactivate", response_model=DoctorRead, status_code=status.HTTP_200_OK
)
def deactivate_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctors_service.set_doctor_active_status(db, doctor_id, False)


@router.patch(
    "/{doctor_id}/activate", response_model=DoctorRead, status_code=status.HTTP_200_OK
)
def activate_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctors_service.set_doctor_active_status(db, doctor_id, True)


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctors_service.delete_doctor(db, doctor_id)
    return None
