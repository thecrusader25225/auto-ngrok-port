from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()
db: Dict[str, str] = {}  # In-memory. Use Redis/SQLite for persistence.

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
