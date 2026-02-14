import uuid
from datetime import datetime, timedelta
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base


class Memory(Base):
    __tablename__ = "memories"

    __table_args__ = (
        Index("idx_memory_vault_id", "vault_id"),
        Index("idx_memory_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    vault_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vaults.id", ondelete="CASCADE"),
        nullable=False
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    memory_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    is_seed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    editable_until: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(hours=8)
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
