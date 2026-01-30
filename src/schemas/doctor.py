from pydantic import BaseModel, Field


class DoctorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    specialization: str = Field(min_length=1, max_length=150)


class DoctorRead(DoctorCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
