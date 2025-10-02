from fastapi import FastAPI, Request
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db: Dict[str, Dict[str, str]] = {}  # device -> {usecase: url}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://your-frontend.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register(request: Request):
    """
    Accepts JSON:
    {
        "device": "device_id",
        "usecase": "http",
        "url": "https://ngrok1"
    }
    Can be called multiple times for the same device with different usecases.
    """
    data = await request.json()
    device = data.get("device")
    usecase = data.get("usecase")
    url = data.get("url")

    if not device or not usecase or not url:
        return {"status": "error", "message": "device, usecase, and url required"}

    # Merge or create
    if device not in db:
        db[device] = {}
    db[device][usecase] = url

    return {"status": "ok", "saved": {device: db[device]}}

@app.get("/get/{device}")
def get_urls(device: str):
    """
    Returns:
    {
        "http": "...",
        "ws": "...",
        "api": "..."
    }
    """
    return {"urls": db.get(device, {"error": "Not found"})}
