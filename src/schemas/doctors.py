from datetime import datetime
from pydantic import BaseModel, Field


class DoctorCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    specialization: str = Field(min_length=1, max_length=100)


class DoctorRead(BaseModel):
    id: int = Field(gt=0)
    full_name: str
    specialization: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
