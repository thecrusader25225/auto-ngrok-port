from fastapi import FastAPI, Request
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db: Dict[str, str] = {}  # In-memory. Use Redis/SQLite for persistence.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://your-frontend.com"] for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/register")
async def register(request: Request):
    data = await request.json()
    device = data.get("device")
    address = data.get("address")
    db[device] = address
    return {"status": "ok", "saved": {device: address}}

@app.get("/get/{device}")
def get_address(device: str):
    return {"address": db.get(device, "Not found")}
