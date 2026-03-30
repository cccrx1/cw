from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReminderCreate(BaseModel):
    pet_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=100)
    reminder_type: str = Field(..., pattern="^(vaccine|checkup|medicine|revisit|other)$")
    remind_at: datetime
    repeat_rule: str = Field(default="none", pattern="^(none|daily|weekly|monthly)$")
    status: str = Field(default="active", pattern="^(active|inactive|done)$")
    source_prediction_id: Optional[int] = None


class ReminderUpdate(BaseModel):
    pet_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    reminder_type: Optional[str] = Field(None, pattern="^(vaccine|checkup|medicine|revisit|other)$")
    remind_at: Optional[datetime] = None
    repeat_rule: Optional[str] = Field(None, pattern="^(none|daily|weekly|monthly)$")
    status: Optional[str] = Field(None, pattern="^(active|inactive|done)$")


class ReminderResponse(BaseModel):
    id: int
    user_id: int
    pet_id: Optional[int]
    title: str
    reminder_type: str
    remind_at: datetime
    repeat_rule: str
    status: str
    source_prediction_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True