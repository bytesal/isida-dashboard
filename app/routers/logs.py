from fastapi import APIRouter
from app.database import db

router = APIRouter()

@router.get("/{guild_id}")
async def get_mod_logs(guild_id: int, limit: int = 50):
    logs_cursor = db.database.mod_logs.find({"guild_id": guild_id}).sort("timestamp", -1).limit(limit)
    logs = await logs_cursor.to_list(length=limit)
    for l in logs:
        l["_id"] = str(l["_id"])
    return logs
