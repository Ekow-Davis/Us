from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.vaults import router as vault_router
from app.api.memories import router as memory_router


app = FastAPI(title="Shared Memory Vault API")


@app.get("/")
def root():
    return {"message": "Vault API running"}

app.include_router(auth_router)
app.include_router(vault_router)
app.include_router(memory_router)