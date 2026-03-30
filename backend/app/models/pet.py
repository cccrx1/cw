from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    species = Column(String(30), nullable=False)  # dog/cat/other
    breed = Column(String(50))
    gender = Column(String(10))  # male/female/unknown
    birth_date = Column(Date, nullable=True)
    weight_kg = Column(Float, nullable=False)
    disease_history = Column(Text)
    vaccine_history = Column(Text)
    note = Column(Text)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="pets")
    predictions = relationship("Prediction", back_populates="pet")
    reminders = relationship("Reminder", back_populates="pet")