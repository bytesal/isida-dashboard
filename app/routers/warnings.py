from fastapi import APIRouter, Request
from app.database import db

router = APIRouter()

@router.get("/{guild_id}")
async def get_warnings(guild_id: int):
    warnings_cursor = db.database.warnings.find({"guild_id": guild_id})
    warnings = await warnings_cursor.to_list(length=100)
    for w in warnings:
        w["_id"] = str(w["_id"])
    return warnings
