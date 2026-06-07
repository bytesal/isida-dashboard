from fastapi import APIRouter, Request, HTTPException
from app.database import db

router = APIRouter()

@router.get("/{guild_id}")
async def get_verification_settings(guild_id: int, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    settings = await db.database.verification_settings.find_one({"guild_id": guild_id})
    if not settings:
        return {"configured": False}
    
    return {
        "configured": True,
        "channel_id": settings.get("channel_id"),
        "role_id": settings.get("role_id"),
        "emoji": settings.get("emoji", "✅"),
        "message_id": str(settings.get("message_id")) if settings.get("message_id") else None
    }

@router.post("/{guild_id}")
async def update_verification_settings(guild_id: int, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    data = await request.json()
    update_data = {}
    if "channel_id" in data:
        update_data["channel_id"] = data["channel_id"]
    if "role_id" in data:
        update_data["role_id"] = data["role_id"]
    if "emoji" in data:
        update_data["emoji"] = data["emoji"]
    
    if update_data:
        await db.database.verification_settings.update_one(
            {"guild_id": guild_id},
            {"$set": update_data},
            upsert=True
        )
    return {"success": True}