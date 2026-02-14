from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class MediaResponse(BaseModel):
    id: uuid.UUID
    file_url: str
    file_type: str

    class Config:
        from_attributes = True


class MemoryCreate(BaseModel):
    title: str
    content: str
    memory_date: datetime | None = None


class MemoryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class MemoryResponse(BaseModel):
    id: uuid.UUID
    vault_id: uuid.UUID
    created_by: uuid.UUID
    title: str
    content: str
    memory_date: datetime | None
    created_at: datetime
    edited_at: datetime | None
    is_seed: bool
    media: list[MediaResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
