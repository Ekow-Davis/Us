from pydantic import BaseModel, EmailStr, validator, Field
import uuid
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    display_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateDisplayNameRequest(BaseModel):
    display_name: str = Field(..., min_length=2, max_length=50)
    
    @validator('display_name')
    def validate_display_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Display name cannot be empty or whitespace only')
        return v.strip()

class UpdateDisplayNameResponse(BaseModel):
    id: str
    display_name: str