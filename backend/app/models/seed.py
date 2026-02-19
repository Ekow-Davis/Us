import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base


class Seed(Base):
    __tablename__ = "seeds"

    __table_args__ = (
        Index("idx_seed_vault_id", "vault_id"),
        Index("idx_seed_bloom_at", "bloom_at"),
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

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    bloom_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="scheduled"  # scheduled | bloomed | cancelled
    )

    bloom_notified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    views = relationship(
        "SeedView",
        backref="seed",
        cascade="all, delete-orphan"
    )

    media = relationship(
        "SeedMedia",
        backref="seed",
        cascade="all, delete-orphan"
    )
