from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    """
    Check server status
    """
    return {"status": "ok", "message": "Server is running"}
