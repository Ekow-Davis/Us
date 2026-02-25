from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from math import ceil

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.notification import Notification
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# Get Endpoint

# Get notifications for the current user with pagination
@router.get("/")
def get_notifications(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc())

    total = query.count()

    notifications = query.offset((page - 1) * page_size)\
                         .limit(page_size)\
                         .all()

    return {
        "items": notifications,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size)
    }

# Mark a notification as read
@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()

    return {"message": "Marked as read"}

# Get count of unread notifications for the current user
@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()

    return {"unread_count": count}

# Cleanup Endpoint
@router.delete("/cleanup")
def cleanup_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == True
    ).delete()

    db.commit()

    return {"message": "Old notifications cleared"}
