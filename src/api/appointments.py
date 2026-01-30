from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.appointments import AppointmentCreate, AppointmentRead
from src.services import appointments as appointments_service

router = APIRouter()


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    return appointments_service.create_appointment(db, payload)


@router.get("", response_model=list[AppointmentRead], status_code=status.HTTP_200_OK)
def list_appointments(
    date: date = Query(..., description="YYYY-MM-DD"),
    doctor_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    return appointments_service.list_appointments(db, date, doctor_id)
