from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vault_membership import VaultMembership
from app.models.thinking_signal import ThinkingSignal

router = APIRouter(prefix="/signals", tags=["Signals"])


def get_user_vault(db: Session, user_id):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == user_id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(status_code=400, detail="Not in active vault")

    return membership.vault_id

# POST ENDPOINTS

# Sending a signal creates a new ThinkingSignal entry for the partner in the vault. 
# The sender is the current user, and the recipient is the other user in the vault. 
# If there is no partner, an error is raised.
@router.post("/send")
def send_signal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    # Find partner
    partner_membership = db.query(VaultMembership).filter(
        VaultMembership.vault_id == vault_id,
        VaultMembership.user_id != current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not partner_membership:
        raise HTTPException(status_code=400, detail="No partner in vault")

    signal = ThinkingSignal(
        vault_id=vault_id,
        sender_id=current_user.id,
        recipient_id=partner_membership.user_id
    )

    db.add(signal)
    db.commit()

    return {"message": "Signal sent"}

# Marking signals as seen updates all unseen signals for the current user to seen and sets the seen_at timestamp.
@router.post("/mark-seen")
def mark_signals_seen(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    signals = db.query(ThinkingSignal).filter(
        ThinkingSignal.recipient_id == current_user.id,
        ThinkingSignal.is_seen == False
    ).all()

    for signal in signals:
        signal.is_seen = True
        signal.seen_at = datetime.utcnow()

    db.commit()

    return {"message": "Signals marked as seen"}


# GET ENDPOINTS

# Getting the unread signal count returns the number of unseen signals for the current user. 
# This can be used to show a notification badge in the frontend.
@router.get("/unread-count")
def get_unread_signal_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(ThinkingSignal).filter(
        ThinkingSignal.recipient_id == current_user.id,
        ThinkingSignal.is_seen == False
    ).count()

    return {"unread_count": count}
