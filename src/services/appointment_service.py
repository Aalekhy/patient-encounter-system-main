# from datetime import datetime, timedelta, timezone
# from sqlalchemy.orm import Session
# from fastapi import HTTPException

# from src.models.appointment import AlekhyaAppointment
# from src.models.doctor import AlekhyaDoctor


# def create_appointment(db: Session, data):
#     now = datetime.now(timezone.utc)

#     if data.start_time <= now:
#         raise HTTPException(status_code=400, detail="Appointment must be in the future")

#     doctor = db.query(AlekhyaDoctor).filter(AlekhyaDoctor.id == data.doctor_id).first()
#     if not doctor or not doctor.is_active:
#         raise HTTPException(status_code=400, detail="Doctor not available")

#     start = data.start_time
#     end = start + timedelta(minutes=data.duration_minutes)

#     overlapping = (
#         db.query(AlekhyaAppointment)
#         .filter(
#             AlekhyaAppointment.doctor_id == data.doctor_id,
#             AlekhyaAppointment.start_time < end,
#             (
#                 AlekhyaAppointment.start_time
#                 + timedelta(minutes=AlekhyaAppointment.duration_minutes)
#             )
#             > start,
#         )
#         .first()
#     )

#     if overlapping:
#         raise HTTPException(status_code=409, detail="overlap appointment")

#     appt = AlekhyaAppointment(**data.dict())
#     db.add(appt)
#     db.commit()
#     db.refresh(appt)
#     return appt
from datetime import datetime, timedelta, timezone
from tracemalloc import start
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.appointment import AlekhyaAppointment
from src.models.doctor import AlekhyaDoctor
from src.models.patient import AlekhyaPatient


def create_appointment(db: Session, data):
    now = datetime.now(timezone.utc)

    # Ensure start_time is in the future
    if data.start_time <= now:
        raise HTTPException(
            status_code=400,
            detail=f"Appointment must be in the future. Provided: {data.start_time}, Now: {now}",
        )

    # Ensure doctor exists and is active
    doctor = db.query(AlekhyaDoctor).filter(AlekhyaDoctor.id == data.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=400, detail=f"Doctor with ID {data.doctor_id} not found"
        )
    if not doctor.is_active:
        raise HTTPException(
            status_code=400, detail=f"Doctor with ID {data.doctor_id} is not active"
        )

    # Ensure patient exists
    patient = (
        db.query(AlekhyaPatient).filter(AlekhyaPatient.id == data.patient_id).first()
    )
    if not patient:
        raise HTTPException(
            status_code=400, detail=f"Patient with ID {data.patient_id} not found"
        )

    # Calculate appointment end time
    # start = data.start_time
    # end = start + timedelta(minutes=int(data.duration_minutes))  # Cast to int
    # Calculate appointment end time
    start = data.start_time
    try:
        # Ensure duration_minutes is extracted as a plain integer
        duration_minutes = int(data.duration_minutes)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid duration_minutes value")
    end = start + timedelta(minutes=duration_minutes)

    # Check for overlapping appointments
    overlapping = (
        db.query(AlekhyaAppointment)
        .filter(
            AlekhyaAppointment.doctor_id == data.doctor_id,
            AlekhyaAppointment.start_time < end,
            (
                AlekhyaAppointment.start_time
                + timedelta(minutes=int(AlekhyaAppointment.duration_minutes))
            )
            > start,
        )
        .first()
    )

    if overlapping:
        raise HTTPException(
            status_code=409,
            detail=f"Overlapping appointment exists for Doctor ID {data.doctor_id}",
        )

    # Create and save the appointment
    appt = AlekhyaAppointment(**data.model_dump())  # Use `model_dump` for Pydantic v2
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt
