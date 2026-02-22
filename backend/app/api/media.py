from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.config.supabase import supabase
from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.memory import Memory
from app.models.memory_media import MemoryMedia
from app.models.vault_membership import VaultMembership

router = APIRouter(prefix="/media", tags=["Media"])

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


def get_user_vault(db: Session, user_id):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == user_id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(status_code=400, detail="User not in active vault")

    return membership.vault_id


@router.post("/{memory_id}")
async def upload_media(
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

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 20MB)")

    extension = file.filename.split(".")[-1]
    file_path = f"memories/{memory_id}/{uuid4()}.{extension}"

    supabase.storage.from_("vault-media").upload(
        file_path,
        contents,
        {"content-type": file.content_type}
    )

    public_url = supabase.storage.from_("vault-media").get_public_url(file_path)

    media = MemoryMedia(
        memory_id=memory.id,
        file_url=public_url,
        file_path=file_path,
        file_type=file.content_type
    )

    db.add(media)
    db.commit()

    return {"message": "File uploaded successfully"}

@router.delete("/{media_id}")
def delete_media(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    media = db.query(MemoryMedia).filter(
        MemoryMedia.id == media_id
    ).first()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    memory = db.query(Memory).filter(
        Memory.id == media.memory_id,
        Memory.is_deleted == False
    ).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Associated memory not found")

    vault_id = get_user_vault(db, current_user.id)

    if memory.vault_id != vault_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if memory.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can delete media")

    if datetime.now(timezone.utc) > memory.editable_until:
        raise HTTPException(status_code=403, detail="Media delete window expired")

    supabase.storage.from_("vault-media").remove([media.file_path])

    db.delete(media)
    db.commit()

    return {"message": "Media deleted successfully"}