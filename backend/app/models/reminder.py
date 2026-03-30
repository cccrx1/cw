from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=True)
    title = Column(String(100), nullable=False)
    reminder_type = Column(String(30), nullable=False)  # vaccine/checkup/medicine/revisit/other
    remind_at = Column(DateTime, nullable=False)
    repeat_rule = Column(String(30), nullable=False, default="none")  # none/daily/weekly/monthly
    status = Column(String(20), nullable=False, default="active")  # active/inactive/done
    source_prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="reminders")
    pet = relationship("Pet", back_populates="reminders")
    source_prediction = relationship("Prediction", back_populates="reminders")