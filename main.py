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
@app.post("/register")
async def register(request: Request):
    data = await request.json()
    device = data.get("device")
    usecase = data.get("usecase")
    url = data.get("url")
    
    if device not in db:
        db[device] = {}
    db[device][usecase] = url  # merge instead of replace

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
