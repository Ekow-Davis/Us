from app.config.supabase import supabase
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from math import ceil

from app.config.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.seed import Seed
from app.models.seed_view import SeedView
from app.models.memory import Memory
from app.models.vault_membership import VaultMembership
from app.schemas.seed import SeedCreate, SeedResponse
from app.models.seed_media import SeedMedia
from app.models.memory_media import MemoryMedia
from app.services.notification import create_notification

SEED_UPLOAD_DIR = "uploads/seeds"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "video/mp4"}
MAX_FILE_SIZE = 20 * 1024 * 1024


router = APIRouter(prefix="/seeds", tags=["Seeds"])

def get_user_vault(db: Session, user_id):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == user_id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(status_code=400, detail="User not in active vault")

    return membership.vault_id


# GET ENDPOINTS

# Get active seeds for the user's vault (not archived, basically the seeds that are still "blooming")
@router.get("/active")
def get_active_seeds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    seeds = db.query(Seed).filter(
        Seed.vault_id == vault_id,
        Seed.status == "scheduled",
        Seed.bloom_at <= datetime.now(timezone.utc)
    ).order_by(Seed.bloom_at.asc()).all()

    result = []

    now = datetime.now(timezone.utc)

    for seed in seeds:
        # If ready AND not yet notified
        if (
            seed.status == "scheduled" and
            seed.bloom_at <= now and
            not seed.bloom_notified
        ):
            # Notify creator if partner hasn't seen yet
            if seed.created_by != current_user.id:
                create_notification(
                    db=db,
                    user_id=seed.created_by,
                    type="seed_ready",
                    title="A Seed is Ready to Bloom 🌸",
                    message="One of your seeds is ready to bloom.",
                    reference_type="seed",
                    reference_id=seed.id
                )

            seed.bloom_notified = True
        
    db.commit()

    return result

# Get a specific seed by ID
@router.get("/{seed_id}")
def get_seed_details(
    seed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    seed = db.query(Seed).filter(
        Seed.id == seed_id,
        Seed.vault_id == vault_id
    ).first()

    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")

    views = db.query(SeedView).filter(
        SeedView.seed_id == seed.id
    ).all()

    viewed_user_ids = {v.user_id for v in views}

    # Media visibility rule
    if seed.created_by == current_user.id:
        media_list = [
            {
                "id": m.id,
                "file_url": m.file_url,
                "file_type": m.file_type
            }
            for m in seed.media
        ]
    else:
        if datetime.now(timezone.utc) >= seed.bloom_at:
            media_list = [
                {
                    "id": m.id,
                    "file_url": m.file_url,
                    "file_type": m.file_type
                }
                for m in seed.media
            ]
        else:
            media_list = []

    return {
        "id": seed.id,
        "title": seed.title,
        "content": seed.content,
        "bloom_at": seed.bloom_at,
        "created_at": seed.created_at,
        "status": seed.status,
        "view_count": len(viewed_user_ids),
        "media": media_list,
        "has_viewed": current_user.id in viewed_user_ids
    }

# Get all seeds for the user's vault (including archived)
@router.get("/")
def get_all_seeds(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    query = db.query(Seed).filter(
        Seed.vault_id == vault_id
    ).order_by(Seed.created_at.desc())

    total = query.count()

    seeds = query.offset((page - 1) * page_size)\
                 .limit(page_size)\
                 .all()

    result = []

    now = datetime.now(timezone.utc)

    for seed in seeds:
        views = db.query(SeedView).filter(
            SeedView.seed_id == seed.id
        ).count()

        is_ready = (
            seed.status == "scheduled" and
            now >= seed.bloom_at
        )

        result.append({
            "id": seed.id,
            "title": seed.title,
            "bloom_at": seed.bloom_at,
            "created_at": seed.created_at,
            "status": seed.status,
            "is_ready": is_ready,
            "memory_id": seed.memory_id,
            "media": [
                {
                    "id": m.id,
                    "file_url": m.file_url,
                    "file_type": m.file_type
                }
                for m in seed.media
            ],
            "view_count": views,
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size)
    }

@router.get("/me")
def get_my_seeds(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    query = db.query(Seed).filter(
        Seed.vault_id == vault_id,
        Seed.created_by == current_user.id
    ).order_by(Seed.created_at.desc())

    total = query.count()

    seeds = query.offset((page - 1) * page_size)\
                 .limit(page_size)\
                 .all()

    now = datetime.now(timezone.utc)

    result = []

    for seed in seeds:
        is_ready = (
            seed.status == "scheduled" and
            now >= seed.bloom_at
        )

        result.append({
            "id": seed.id,
            "title": seed.title,
            "bloom_at": seed.bloom_at,
            "created_at": seed.created_at,
            "status": seed.status,
            "is_ready": is_ready,
            "memory_id": seed.memory_id,
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size)
    }

@router.get("/summary")
def get_seed_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    now = datetime.now(timezone.utc)

    # Total (exclude cancelled)
    total = db.query(func.count(Seed.id)).filter(
        Seed.vault_id == vault_id,
        Seed.status != "cancelled"
    ).scalar()

    # Growing (scheduled + future)
    growing = db.query(func.count(Seed.id)).filter(
        Seed.vault_id == vault_id,
        Seed.status == "scheduled",
        Seed.bloom_at > now
    ).scalar()

    # Ready (scheduled + past bloom time)
    ready = db.query(func.count(Seed.id)).filter(
        Seed.vault_id == vault_id,
        Seed.status == "scheduled",
        Seed.bloom_at <= now
    ).scalar()

    # Bloomed (converted)
    bloomed = db.query(func.count(Seed.id)).filter(
        Seed.vault_id == vault_id,
        Seed.status == "bloomed"
    ).scalar()

    return {
        "total": total,
        "growing": growing,
        "ready": ready,
        "bloomed": bloomed
    }

# POST ENDPOINTS

# Only allow users in the vault to create seeds
@router.post("/", response_model=SeedResponse)
def create_seed(
    seed_data: SeedCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = db.query(VaultMembership).filter(
        VaultMembership.user_id == current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if not membership:
        raise HTTPException(status_code=400, detail="Not in vault")

    if seed_data.bloom_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Bloom date must be in the future"
        )

    seed = Seed(
        vault_id=membership.vault_id,
        created_by=current_user.id,
        title=seed_data.title,
        content=seed_data.content,
        bloom_at=seed_data.bloom_at
    )

    db.add(seed)
    db.flush()  # so we get seed.id without committing yet

    # Find partner
    partner = db.query(VaultMembership).filter(
        VaultMembership.vault_id == membership.vault_id,
        VaultMembership.user_id != current_user.id,
        VaultMembership.left_at.is_(None)
    ).first()

    if partner:
        create_notification(
            db=db,
            user_id=partner.user_id,
            type="seed_created",
            title="New Seed Planted",
            message="Your partner planted a new seed.",
            reference_type="seed",
            reference_id=seed.id
        )

    db.commit()
    db.refresh(seed)

    return seed

# Endpoint to bloom a seed (mark as viewed by current user)
@router.post("/{seed_id}/bloom")
def bloom_seed(
    seed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    seed = db.query(Seed).filter(
        Seed.id == seed_id,
        Seed.vault_id == vault_id,
        Seed.status == "scheduled"
    ).first()

    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")

    if datetime.now(timezone.utc) < seed.bloom_at:
        raise HTTPException(status_code=400, detail="Seed not ready")

    # Record view if not already viewed
    existing_view = db.query(SeedView).filter(
        SeedView.seed_id == seed.id,
        SeedView.user_id == current_user.id
    ).first()

    if not existing_view:
        db.add(
            SeedView(
                seed_id=seed.id,
                user_id=current_user.id
            )
        )
        db.commit()

    # Recalculate total views
    total_views = db.query(SeedView).filter(
        SeedView.seed_id == seed.id
    ).count()

    if total_views >= 2:

        if seed.status != "scheduled":
            return {"status": "already_converted"}

        memory = Memory(
            vault_id=seed.vault_id,
            created_by=seed.created_by,
            title=seed.title,
            content=seed.content,
            is_seed=True
        )

        db.add(memory)
        db.flush()

        for seed_media in seed.media:
            db.add(
                MemoryMedia(
                    memory_id=memory.id,
                    file_url=seed_media.file_url,
                    file_type=seed_media.file_type
                )
            )

        seed.status = "bloomed"

        db.commit()

        return {"status": "converted_to_memory"}

    return {"status": "view_recorded"}


# Endpoint to upload media for a seed
@router.post("/{seed_id}/media")
async def upload_seed_media(
    seed_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    seed = db.query(Seed).filter(
        Seed.id == seed_id,
        Seed.vault_id == vault_id,
        Seed.status == "scheduled"
    ).first()

    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")

    # Only creator can upload
    if seed.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Edit window check (24h)
    if datetime.now(timezone.utc) > seed.created_at + timedelta(hours=24):
        raise HTTPException(status_code=403, detail="Edit window expired")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    extension = file.filename.split(".")[-1]
    file_path = f"memories/{seed_id}/{uuid4()}.{extension}"

    supabase.storage.from_("vault-media").upload(
        file_path,
        contents,
        {"content-type": file.content_type}
    )

    media = SeedMedia(
        seed_id=seed.id,
        file_url=supabase.storage.from_("vault-media").get_public_url(file_path),
        file_type=file.content_type,
        file_path=file_path
    )

    db.add(media)
    db.commit()

    return {"message": "Seed media uploaded"}


# DELETE ENDPOINTS
@router.delete("/media/{media_id}")
def delete_seed_media(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    media = db.query(SeedMedia).filter(
        SeedMedia.id == media_id
    ).first()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    vault_id = get_user_vault(db, current_user.id)

    seed = db.query(Seed).filter(
        Seed.id == media.seed_id,
        Seed.vault_id == vault_id
    ).first()

    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")

    if seed.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if datetime.now(timezone.utc) > seed.created_at + timedelta(hours=24):
        raise HTTPException(status_code=403, detail="Delete window expired")

    file_path = media.file_path
    supabase.storage.from_("vault-media").remove([file_path])

    db.delete(media)
    db.commit()

    return {"message": "Seed media deleted"}


# PUT ENDPOINTS

# Only allow users in the vault to update seeds, and only within 24h of creation and before bloom time
@router.put("/{seed_id}")
def update_seed(
    seed_id: str,
    seed_data: SeedCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    seed = db.query(Seed).filter(
        Seed.id == seed_id,
        Seed.vault_id == vault_id,
        Seed.status == "scheduled"
    ).first()

    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")

    if seed.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can edit")

    if datetime.now(timezone.utc) > seed.created_at + timedelta(hours=24):
        raise HTTPException(status_code=403, detail="Edit window expired")

    if datetime.now(timezone.utc) >= seed.bloom_at:
        raise HTTPException(status_code=403, detail="Cannot edit after bloom")

    seed.title = seed_data.title
    seed.content = seed_data.content
    seed.bloom_at = seed_data.bloom_at
    seed.edited_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(seed)

    return {"message": "Seed updated successfully"}


# DELETE ENDPOINTS

# Only allow the creator of the seed in the vault to delete seeds, and only within 24h of creation or at least 24h before bloom time
@router.delete("/{seed_id}")
def cancel_seed(
    seed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vault_id = get_user_vault(db, current_user.id)

    seed = db.query(Seed).filter(
        Seed.id == seed_id,
        Seed.vault_id == vault_id,
        Seed.status == "scheduled"
    ).first()

    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")

    if seed.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can cancel")

    now = datetime.now(timezone.utc)

    within_creation_window = now <= seed.created_at + timedelta(hours=24)
    before_bloom_cutoff = now <= seed.bloom_at - timedelta(hours=24)

    if not (within_creation_window or before_bloom_cutoff):
        raise HTTPException(status_code=403, detail="Cancel window expired")

    seed.status = "cancelled"

    db.commit()

    return {"message": "Seed cancelled successfully"}
