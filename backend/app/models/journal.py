import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base
from sqlalchemy.orm import relationship


class Journal(Base):
    __tablename__ = "journals"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    vault_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("vaults.id", ondelete="CASCADE"),
        nullable=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    visibility: Mapped[str] = mapped_column(
        String(20),
        default="private"  # private | shared
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active"  # active | converted
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    memory_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("memories.id", ondelete="SET NULL"),
        nullable=True
    )

    memory = relationship("Memory")

