from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class PatientCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=20)


class PatientRead(BaseModel):
    id: int = Field(gt=0)
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
