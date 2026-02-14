import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vault import Vault
from app.models.vault_membership import VaultMembership

router = APIRouter(prefix="/vaults", tags=["Vaults"])

@router.post("/create")
def create_vault(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user already in active vault
    existing_membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already belongs to a vault"
        )

    while True:
      invite_code = secrets.token_hex(4)
      exists = db.query(Vault).filter(
          Vault.invite_code == invite_code
      ).first()
      if not exists:
          break


    vault = Vault(
        invite_code=invite_code,
        status="pending"
    )

    db.add(vault)
    db.commit()
    db.refresh(vault)

    membership = VaultMembership(
        vault_id=vault.id,
        user_id=current_user.id
    )

    db.add(membership)
    db.commit()

    return {
        "vault_id": vault.id,
        "invite_code": vault.invite_code
    }

@router.post("/join/{invite_code}")
def join_vault(
    invite_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault = db.query(Vault).filter(
        Vault.invite_code == invite_code
    ).first()

    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invite code"
        )
    
    if vault.status == "archived":
      raise HTTPException(
          status_code=400,
          detail="Vault is archived"
      )
    
    existing_membership = db.query(VaultMembership).filter(
    VaultMembership.user_id == current_user.id,
    VaultMembership.left_at.is_(None)
    ).first()

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in a vault"
        )

    # Count active members
    active_members = db.query(VaultMembership).filter(
        VaultMembership.vault_id == vault.id,
        VaultMembership.left_at.is_(None)
    ).count()

    if active_members >= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vault already has 2 users"
        )

    membership = VaultMembership(
        vault_id=vault.id,
        user_id=current_user.id
    )

    db.add(membership)

    if active_members == 1:
        vault.status = "active"




    db.commit()

    return {"message": "Joined vault successfully"}

@router.get("/me")
def get_my_vault(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        return {"vault": None}

    vault = db.query(Vault).filter(
        Vault.id == membership.vault_id
    ).first()

    return {
        "vault_id": vault.id,
        "status": vault.status,
        "invite_code": vault.invite_code
    }

from datetime import datetime

@router.post("/leave")
def leave_vault(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(
            status_code=400,
            detail="User not in a vault"
        )

    membership.left_at = datetime.utcnow()
    db.commit()

    # Check remaining active members
    active_members = db.query(VaultMembership).filter(
        VaultMembership.vault_id == membership.vault_id,
        VaultMembership.left_at.is_(None)
    ).count()

    vault = db.query(Vault).filter(
        Vault.id == membership.vault_id
    ).first()

    if active_members == 1:
        vault.status = "pending"
    elif active_members == 0:
        vault.status = "archived"

    db.commit()

    return {"message": "Left vault successfully"}
