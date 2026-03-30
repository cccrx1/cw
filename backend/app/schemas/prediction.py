from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any


class RecommendedReminder(BaseModel):
    title: str
    reminder_type: str = Field(..., pattern="^(vaccine|checkup|medicine|revisit|other)$")
    days_from_now: int = Field(..., ge=0)


class PredictionCreate(BaseModel):
    pet_id: int


class PredictionResponse(BaseModel):
    id: int
    user_id: int
    pet_id: int
    risk_level: str
    summary: str
    suggestion: str
    risk_factors: List[str]
    recommended_reminders: List[RecommendedReminder]
    created_at: datetime
    
    class Config:
        from_attributes = True