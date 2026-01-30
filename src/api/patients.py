from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.patients import PatientCreate, PatientRead
from src.services import patients as patients_service

router = APIRouter()


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = patients_service.create_patient(db, payload)
    return patient


@router.get("/{patient_id}", response_model=PatientRead, status_code=status.HTTP_200_OK)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = patients_service.get_patient(db, patient_id)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patients_service.delete_patient(db, patient_id)
    return None
