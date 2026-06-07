from fastapi import APIRouter, Request, HTTPException
from app.database import db

router = APIRouter()

@router.get("/{guild_id}")
async def get_mod_logs(guild_id: int, request: Request, limit: int = 100):
    user_token = request.session.get("access_token")
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    logs_cursor = db.database.mod_logs.find({"guild_id": guild_id}).sort("timestamp", -1).limit(limit)
    logs = await logs_cursor.to_list(length=limit)
    for l in logs:
        l["_id"] = str(l["_id"])
        if "timestamp" in l and hasattr(l["timestamp"], "isoformat"):
            l["timestamp"] = l["timestamp"].isoformat()
    return logs
