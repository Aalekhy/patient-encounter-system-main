from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.appointment import AlekhyaAppointment
from src.models.doctor import AlekhyaDoctor


def create_appointment(db: Session, data):
    now = datetime.now(timezone.utc)

    if data.start_time <= now:
        raise HTTPException(status_code=400, detail="Appointment must be in the future")

    doctor = db.query(AlekhyaDoctor).filter(AlekhyaDoctor.id == data.doctor_id).first()
    if not doctor or not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor not available")

    start = data.start_time
    end = start + timedelta(minutes=data.duration_minutes)

    overlapping = (
        db.query(AlekhyaAppointment)
        .filter(
            AlekhyaAppointment.doctor_id == data.doctor_id,
            AlekhyaAppointment.start_time < end,
            (
                AlekhyaAppointment.start_time
                + timedelta(minutes=AlekhyaAppointment.duration_minutes)
            )
            > start,
        )
        .first()
    )

    if overlapping:
        raise HTTPException(status_code=409, detail="Overlapping appointment")

    appt = AlekhyaAppointment(**data.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt
