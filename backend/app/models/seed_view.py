import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base


class SeedView(Base):
    __tablename__ = "seed_views"

    __table_args__ = (
        UniqueConstraint("seed_id", "user_id", name="uq_seed_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    seed_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("seeds.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
