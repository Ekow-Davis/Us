import uuid
from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.config.database import Base
from sqlalchemy import UniqueConstraint


class VaultMembership(Base):
    __tablename__ = "vault_memberships"

    __table_args__ = (
        UniqueConstraint("vault_id", "user_id", name="uq_vault_user"),
        Index("idx_vault_id", "vault_id"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    vault_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vaults.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    left_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
