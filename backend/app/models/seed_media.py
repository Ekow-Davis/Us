import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base


class SeedMedia(Base):
    __tablename__ = "seed_media"

    __table_args__ = (
        Index("idx_seed_media_seed_id", "seed_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    seed_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("seeds.id", ondelete="CASCADE"),
        nullable=False
    )

    file_url: Mapped[str] = mapped_column(String(500), nullable=False)

    # NEW
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    file_type: Mapped[str] = mapped_column(String(50), nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )