from pydantic import BaseModel, EmailStr
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
