from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AppointmentCreate(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    start_time: datetime
    duration_minutes: int = Field(ge=15, le=180)

    @field_validator("start_time")
    @classmethod
    def timezone_aware_datetime(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError(
                "start_time must be timezone-aware (include timezone offset)"
            )
        return v


class AppointmentRead(BaseModel):
    id: int = Field(gt=0)
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
