from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.memory import Memory
from app.models.vault_membership import VaultMembership
from app.schemas.memory import MemoryCreate, MemoryUpdate, MemoryResponse

router = APIRouter(prefix="/memories", tags=["Memories"])

def get_user_vault(db: Session, user_id):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == user_id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(
            status_code=400,
            detail="User not in an active vault"
        )

    return membership.vault_id


@router.post("/", response_model=MemoryResponse)
def create_memory(
    memory_data: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    memory = Memory(
        vault_id=vault_id,
        created_by=current_user.id,
        title=memory_data.title,
        content=memory_data.content,
        memory_date=memory_data.memory_date,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


@router.get("/", response_model=list[MemoryResponse])
def list_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    memories = db.query(Memory).filter(
        Memory.vault_id == vault_id,
        Memory.is_deleted == False
    ).order_by(Memory.created_at.desc()).all()

    return memories


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(
    memory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    memory = db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.vault_id == vault_id,
        Memory.is_deleted == False
    ).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    return memory


@router.put("/{memory_id}", response_model=MemoryResponse)
def update_memory(
    memory_id: str,
    update_data: MemoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    memory = db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.vault_id == vault_id,
        Memory.is_deleted == False
    ).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    if memory.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only creator can edit memory"
        )

    if datetime.utcnow() > memory.editable_until:
        raise HTTPException(
            status_code=403,
            detail="Memory edit window expired"
        )

    if update_data.title is not None:
        memory.title = update_data.title

    if update_data.content is not None:
        memory.content = update_data.content

    memory.edited_at = datetime.utcnow()

    db.commit()
    db.refresh(memory)

    return memory
