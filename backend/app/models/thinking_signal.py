import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base


class ThinkingSignal(Base):
    __tablename__ = "thinking_signals"

    __table_args__ = (
        Index("idx_signal_vault_id", "vault_id"),
        Index("idx_signal_recipient", "recipient_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    vault_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vaults.id", ondelete="CASCADE"),
        nullable=False
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    recipient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    is_seen: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    seen_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
