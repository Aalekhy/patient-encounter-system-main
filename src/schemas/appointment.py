from datetime import datetime
from pydantic import BaseModel, Field, validator


class AppointmentCreate(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    start_time: datetime
    duration_minutes: int = Field(ge=15, le=180)

    @validator("start_time")
    def must_be_timezone_aware(cls, v):
        if v.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")
        return v


class AppointmentRead(AppointmentCreate):
    id: int

    class Config:
        orm_mode = True
