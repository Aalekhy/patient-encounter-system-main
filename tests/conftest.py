# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from src.database import Base, get_db
# from src.main import app

# # Use SQLite ONLY for tests
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create fresh tables for tests
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


# @pytest.fixture(scope="session")
# def client():
#     return TestClient(app)


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base, get_db
from src.main import app
from src.models.patient import AlekhyaPatient
from src.models.doctor import AlekhyaDoctor

# Use SQLite ONLY for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create fresh tables for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def seed_database():
    """Seed the test database with initial data."""
    db = TestingSessionLocal()
    db.add(
        AlekhyaPatient(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john.doe@test.com",
            phone="1234567890",
        )
    )
    db.add(
        AlekhyaDoctor(
            id=1, name="Dr. Smith", specialization="Cardiology", is_active=True
        )
    )
    db.commit()
    db.close()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
