from fastapi import FastAPI
from app.api.router import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/health")
def health_check():
    """
    Check server status
    """
    return {"status": "ok", "message": "Server is running"}
