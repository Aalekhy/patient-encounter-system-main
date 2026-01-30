from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.doctor import AlekhyaDoctor as Doctor
from src.models.appointment import AlekhyaAppointment as Appointment


def create_doctor(db: Session, data):
    doctor = Doctor(**data.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def deactivate_doctor(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)

    active_appointments = (
        db.query(Appointment).filter(Appointment.doctor_id == doctor_id).first()
    )
    if active_appointments:
        raise HTTPException(status_code=400, detail="Doctor has existing appointments")

    doctor.is_active = False
    db.commit()
    return doctor
