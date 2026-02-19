import uuid
from sqlalchemy.orm import Session
from app.models.notification import Notification
from datetime import datetime, timezone


def create_notification(
    db: Session,
    user_id: uuid.UUID,
    type: str,
    title: str,
    message: str,
    reference_type: str = None,
    reference_id: uuid.UUID = None,
):
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        reference_type=reference_type,
        reference_id=reference_id,
    )

    db.add(notification)
