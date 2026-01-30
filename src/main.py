from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from src.database import Base, engine, get_db

# Schemas
from src.schemas.patient import PatientCreate, PatientRead
from src.schemas.doctor import DoctorCreate, DoctorRead
from src.schemas.appointment import AppointmentCreate, AppointmentRead

# Services
from src.services.patient_service import create_patient, get_patient
from src.services.doctor_service import create_doctor, get_doctor, deactivate_doctor
from src.services.appointment_service import create_appointment

# Models
from src.models.appointment import AlekhyaAppointment as Appointment

# --------------------------------------------------
# CREATE APP
# --------------------------------------------------
app = FastAPI(
    title="Medical Encounter Management System (MEMS)",
    version="1.0.0",
    description="Production-grade FastAPI backend for medical encounters",
)

# --------------------------------------------------
# CREATE TABLES
# --------------------------------------------------
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# ROOT & HEALTH (VERY IMPORTANT)
# --------------------------------------------------
@app.get("/")
def root():
    return {"message": "MEMS FastAPI is running", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "UP"}


# --------------------------------------------------
# PATIENT APIs
# --------------------------------------------------
@app.post("/patients", response_model=PatientRead, status_code=201)
def create_patient_api(payload: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, payload)


@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient_api(patient_id: int, db: Session = Depends(get_db)):
    return get_patient(db, patient_id)


# --------------------------------------------------
# DOCTOR APIs
# --------------------------------------------------
@app.post("/doctors", response_model=DoctorRead, status_code=201)
def create_doctor_api(payload: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, payload)


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def get_doctor_api(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor(db, doctor_id)


@app.patch("/doctors/{doctor_id}/deactivate", response_model=DoctorRead)
def deactivate_doctor_api(doctor_id: int, db: Session = Depends(get_db)):
    return deactivate_doctor(db, doctor_id)


# --------------------------------------------------
# APPOINTMENT APIs
# --------------------------------------------------
@app.post("/appointments", response_model=AppointmentRead, status_code=201)
def create_appointment_api(payload: AppointmentCreate, db: Session = Depends(get_db)):
    return create_appointment(db, payload)


@app.get("/appointments", response_model=list[AppointmentRead])
def list_appointments_api(
    date_: date = Query(..., alias="date"),
    doctor_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Appointment)

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    query = query.filter(Appointment.start_time.cast(date) == date_)
    return query.all()
