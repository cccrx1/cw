from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    input_snapshot = Column(JSON, nullable=False)
    risk_level = Column(String(20), nullable=False)  # low/medium/high
    summary = Column(Text, nullable=False)
    suggestion = Column(Text, nullable=False)
    raw_response = Column(JSON, nullable=False)
    provider = Column(String(30), nullable=False, default="dify")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="predictions")
    pet = relationship("Pet", back_populates="predictions")
    reminders = relationship("Reminder", back_populates="source_prediction")