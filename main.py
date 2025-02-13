from fastapi import FastAPI
from app.api.router import router
from threading import Thread
from app.core.modbus_thread import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_client_list()

@app.get("/health")
def health_check():
    """
    Check server status
    """
    return {"status": "ok", "message": "Server is running"}

@app.on_event("startup")
def startup_event():
    thread = Thread(target = sensor_polling, daemon=True)
    thread.start()
