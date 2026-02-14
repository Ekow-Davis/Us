import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.memory import Memory
from app.models.memory_media import MemoryMedia
from app.models.vault_membership import VaultMembership

router = APIRouter(prefix="/media", tags=["Media"])

UPLOAD_DIR = "uploads/memories"

def get_user_vault(db: Session, user_id):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == user_id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(status_code=400, detail="User not in active vault")

    return membership.vault_id

@router.post("/{memory_id}")
def upload_media(
    memory_id: str,
    file: UploadFile = File(...),
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

    # Create memory-specific folder
    memory_folder = os.path.join(UPLOAD_DIR, memory_id)
    os.makedirs(memory_folder, exist_ok=True)

    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(memory_folder, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save DB record
    media = MemoryMedia(
        memory_id=memory.id,
        file_url=f"/uploads/memories/{memory_id}/{unique_filename}",
        file_type=file.content_type
    )

    db.add(media)
    db.commit()

    return {"message": "File uploaded successfully"}

