from fastapi import FastAPI

app = FastAPI(title="Shared Memory Vault API")


@app.get("/")
def root():
    return {"message": "Vault API running"}
