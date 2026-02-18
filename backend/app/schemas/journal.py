from pydantic import BaseModel
from datetime import datetime
import uuid


class JournalCreate(BaseModel):
    title: str
    content: str
    visibility: str = "private"


class JournalUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    visibility: str | None = None


class JournalResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    visibility: str
    status: str
    created_at: datetime
    edited_at: datetime | None

    class Config:
        from_attributes = True
