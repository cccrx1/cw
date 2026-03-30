from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class PetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    species: str = Field(..., pattern="^(dog|cat|other)$")
    breed: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] = Field(None, pattern="^(male|female|unknown)$")
    birth_date: Optional[date] = None
    weight_kg: float = Field(..., gt=0)
    disease_history: Optional[str] = None
    vaccine_history: Optional[str] = None
    note: Optional[str] = None


class PetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    species: Optional[str] = Field(None, pattern="^(dog|cat|other)$")
    breed: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] = Field(None, pattern="^(male|female|unknown)$")
    birth_date: Optional[date] = None
    weight_kg: Optional[float] = Field(None, gt=0)
    disease_history: Optional[str] = None
    vaccine_history: Optional[str] = None
    note: Optional[str] = None


class PetResponse(BaseModel):
    id: int
    user_id: int
    name: str
    species: str
    breed: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]
    weight_kg: float
    disease_history: Optional[str]
    vaccine_history: Optional[str]
    note: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True