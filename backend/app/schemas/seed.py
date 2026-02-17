from pydantic import BaseModel
from datetime import datetime
import uuid


class SeedCreate(BaseModel):
    title: str
    content: str
    bloom_at: datetime


class SeedResponse(BaseModel):
    id: uuid.UUID
    vault_id: uuid.UUID
    created_by: uuid.UUID
    title: str
    content: str
    bloom_at: datetime
    created_at: datetime
    edited_at: datetime | None
    status: str

    class Config:
        from_attributes = True
