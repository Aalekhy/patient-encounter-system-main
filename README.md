# Medical Encounter Management System (MEMS)

Production-grade backend system for managing patients, doctors, and appointments.

## Tech Stack
- FastAPI
- SQLAlchemy
- MySQL
- Pytest
- GitHub Actions CI

## Features
- Patient management
- Doctor management with activation/deactivation
- Appointment scheduling with conflict prevention
- Timezone-aware datetime handling

## Run Locally
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
