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
        "urls": {
            "http": "https://ngrok1",
            "ws": "https://ngrok2",
            "api": "https://ngrok3"
        }
    }
    """
    data = await request.json()
    device = data.get("device")
    urls = data.get("urls", {})

    # Validate
    if not device or not isinstance(urls, dict) or len(urls) == 0:
        return {"status": "error", "message": "Device and urls dict required"}

    db[device] = urls
    return {"status": "ok", "saved": {device: urls}}

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
