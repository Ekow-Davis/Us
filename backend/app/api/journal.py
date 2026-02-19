from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from math import ceil

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.journal import Journal
from app.models.memory import Memory
from app.models.vault_membership import VaultMembership
from app.schemas.journal import JournalCreate, JournalUpdate, JournalResponse
from app.schemas import memory
from app.services.notification import create_notification

router = APIRouter(prefix="/journals", tags=["Journals"])

def get_user_vault(db: Session, user_id):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == user_id,
        VaultMembership.left_at.is_(None)
    ).first()

    return membership.vault_id if membership else None

# POST ENDPOINTS

# Creating a journal with title, content, and visibility (private/shared). 
# If shared, must be in an active vault and journal gets associated with that vault
@router.post("/", response_model=JournalResponse)
def create_journal(
    journal_data: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = None

    if journal_data.visibility == "shared":
        vault_id = get_user_vault(db, current_user.id)
        if not vault_id:
            raise HTTPException(
                status_code=400,
                detail="Must be in active vault to create shared journal"
            )

    journal = Journal(
        user_id=current_user.id,
        vault_id=vault_id,
        title=journal_data.title,
        content=journal_data.content,
        visibility=journal_data.visibility
    )

    db.add(journal)
    db.commit()
    db.refresh(journal)

    if journal.visibility == "shared" and journal.vault_id:
        partner = db.query(VaultMembership).filter(
            VaultMembership.vault_id == journal.vault_id,
            VaultMembership.user_id != current_user.id,
            VaultMembership.left_at.is_(None)
        ).first()

    if partner:
        create_notification(
            db=db,
            user_id=partner.user_id,
            type="journal_shared",
            title="Journal Shared",
            message="Your partner shared a journal entry.",
            reference_type="journal",
            reference_id=journal.id
        )

    db.commit()

    return journal

# Changing a journal's status from active to converted, and creating a new Memory in the same vault with the same content where this journal becomes read only
@router.post("/{journal_id}/convert")
def convert_journal_to_memory(
    journal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.is_deleted == False
    ).first()

    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    if journal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can convert")

    if journal.status != "active":
        raise HTTPException(status_code=400, detail="Already converted")

    if not journal.vault_id:
        raise HTTPException(
            status_code=400,
            detail="Journal must be shared before converting"
        )

    memory = Memory(
        vault_id=journal.vault_id,
        created_by=journal.user_id,
        title=journal.title,
        content=journal.content,
        is_seed=False
    )

    db.add(memory)
    db.flush()  # get memory.id

    journal.status = "converted"
    journal.memory_id = memory.id

    db.commit()

    partner = db.query(VaultMembership).filter(
        VaultMembership.vault_id == journal.vault_id,
        VaultMembership.user_id != current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if partner:
        create_notification(
            db=db,
            user_id=partner.user_id,
            type="journal_converted",
            title="Journal Became Memory ✨",
            message="A shared journal was converted into a memory.",
            reference_type="memory",
            reference_id=memory.id
        )
    db.commit()

    return {
        "message": "Journal converted to memory",
        "memory_id": memory.id
    }


# GET ENDPOINTS

# Getting all private Journals for the user, sorted by creation date (newest to oldest)
@router.get("/private")
def get_private_journals(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Journal).filter(
        Journal.user_id == current_user.id,
        Journal.visibility == "private",
        Journal.is_deleted == False
    ).order_by(Journal.created_at.desc())

    total = query.count()

    journals = query.offset((page - 1) * page_size)\
                    .limit(page_size)\
                    .all()

    return {
        "items": journals,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size)
    }


# Getting all shared Journals in the user's vault, sorted by creation date (newest to oldest)
@router.get("/shared")
def get_shared_journals(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    query = db.query(Journal).filter(
        Journal.vault_id == vault_id,
        Journal.visibility == "shared",
        Journal.is_deleted == False
    ).order_by(Journal.created_at.desc())

    total = query.count()

    journals = query.offset((page - 1) * page_size)\
                    .limit(page_size)\
                    .all()

    return {
        "items": journals,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size)
    }

@router.get("/analytics/me")
def get_my_journal_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Journal).filter(
        Journal.user_id == current_user.id,
        Journal.is_deleted == False
    ).count()

    private_count = db.query(Journal).filter(
        Journal.user_id == current_user.id,
        Journal.visibility == "private",
        Journal.is_deleted == False
    ).count()

    shared_count = db.query(Journal).filter(
        Journal.user_id == current_user.id,
        Journal.visibility == "shared",
        Journal.is_deleted == False
    ).count()

    converted_count = db.query(Journal).filter(
        Journal.user_id == current_user.id,
        Journal.status == "converted",
        Journal.is_deleted == False
    ).count()

    first_entry = db.query(Journal.created_at).filter(
        Journal.user_id == current_user.id,
        Journal.is_deleted == False
    ).order_by(Journal.created_at.asc()).first()

    latest_entry = db.query(Journal.created_at).filter(
        Journal.user_id == current_user.id,
        Journal.is_deleted == False
    ).order_by(Journal.created_at.desc()).first()

    return {
        "total_entries": total,
        "private_entries": private_count,
        "shared_entries": shared_count,
        "converted_entries": converted_count,
        "first_entry_date": first_entry[0] if first_entry else None,
        "latest_entry_date": latest_entry[0] if latest_entry else None
    }

@router.get("/analytics/vault")
def get_vault_journal_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    if not vault_id:
        raise HTTPException(status_code=400, detail="Not in vault")

    total_shared = db.query(Journal).filter(
        Journal.vault_id == vault_id,
        Journal.visibility == "shared",
        Journal.is_deleted == False
    ).count()

    total_converted = db.query(Journal).filter(
        Journal.vault_id == vault_id,
        Journal.status == "converted",
        Journal.is_deleted == False
    ).count()

    return {
        "total_shared_journals": total_shared,
        "converted_to_memories": total_converted
    }


# PUT ENDPOINTS

# Owner being able to update a journal's title, content, and visibility (private/shared)
@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(
    journal_id: str,
    journal_data: JournalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.is_deleted == False
    ).first()

    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    if journal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can edit")

    if journal.status != "active":
        raise HTTPException(status_code=400, detail="Cannot edit converted journal")

    if journal_data.title is not None:
        journal.title = journal_data.title

    if journal_data.content is not None:
        journal.content = journal_data.content

    if journal_data.visibility is not None:
        if journal_data.visibility == "shared":
            vault_id = get_user_vault(db, current_user.id)
            if not vault_id:
                raise HTTPException(
                    status_code=400,
                    detail="Must be in active vault to share"
                )
            journal.vault_id = vault_id

        if journal_data.visibility == "private":
            journal.vault_id = None

        journal.visibility = journal_data.visibility

    journal.edited_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(journal)

    return journal


# DELETE ENDPOINTS

# Soft deleting a journal by setting is_deleted to True. Only the owner can delete
@router.delete("/{journal_id}")
def delete_journal(
    journal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.is_deleted == False
    ).first()

    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    if journal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can delete")

    journal.is_deleted = True
    db.commit()

    return {"message": "Journal deleted"}
