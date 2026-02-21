from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.vaults import router as vault_router
from app.api.memories import router as memory_router
from app.api.media import router as media_router
from app.api.seed import router as seed_router
from app.api.signals import router as thinking_router
from app.api.journal import router as journal_router
from app.api.notifications import router as notifications_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Shared Memory Vault API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Vault API running"}

app.include_router(auth_router)
app.include_router(vault_router)
app.include_router(memory_router)
app.include_router(media_router)
app.include_router(seed_router)
app.include_router(thinking_router)
app.include_router(journal_router)
app.include_router(notifications_router)

