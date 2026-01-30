from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.database import Base


class AlekhyaDoctor(Base):
    __tablename__ = "Alekhya_doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    specialization = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
