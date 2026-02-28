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

from app.config.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from slowapi.middleware import SlowAPIMiddleware


app = FastAPI(title="Shared Memory Vault API", redirect_slashes=False)

app.add_middleware(SlowAPIMiddleware)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://us-vault.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
