from fastapi import APIRouter, Request, HTTPException
from app.database import db
import httpx
import os

router = APIRouter()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

@router.get("/{guild_id}")
async def get_warnings(guild_id: int, request: Request):
    user_token = request.session.get("access_token")
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    warnings_cursor = db.database.warnings.find({"guild_id": guild_id})
    warnings = await warnings_cursor.to_list(length=200)

    if not warnings:
        return []

    # Fetch moderator usernames
    mod_ids = list(set(w["moderator_id"] for w in warnings))
    async with httpx.AsyncClient() as client:
        mod_names = {}
        for uid in mod_ids:
            try:
                resp = await client.get(
                    f"https://discord.com/api/users/{uid}",
                    headers={"Authorization": f"Bot {BOT_TOKEN}"}
                )
                if resp.status_code == 200:
                    user_data = resp.json()
                    mod_names[uid] = f"{user_data['username']}#{user_data.get('discriminator', '0')}"
                else:
                    mod_names[uid] = f"Unknown ({uid})"
            except:
                mod_names[uid] = f"Unknown ({uid})"

    result = []
    for w in warnings:
        result.append({
            "_id": str(w["_id"]),
            "guild_id": w["guild_id"],
            "user_id": w["user_id"],
            "moderator_id": w["moderator_id"],
            "moderator_name": mod_names.get(w["moderator_id"], f"Unknown ({w['moderator_id']})"),
            "reason": w["reason"],
            "timestamp": w["timestamp"].isoformat() if hasattr(w["timestamp"], "isoformat") else w["timestamp"]
        })
    return result
