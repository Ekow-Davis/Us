from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(title="Shared Memory Vault API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Vault API running"}
