import uuid
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.config.database import Base


class Vault(Base):
    __tablename__ = "vaults"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    invite_code: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )
