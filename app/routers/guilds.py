from fastapi import APIRouter, Request, HTTPException
import httpx
import os

router = APIRouter()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

@router.get("/")
async def list_guilds(request: Request):
    user_token = request.session.get("access_token")
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    async with httpx.AsyncClient() as client:
        # Fetch user's guilds
        user_guilds_resp = await client.get(
            "https://discord.com/api/users/@me/guilds",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        user_guilds = user_guilds_resp.json()
        
        # Fetch bot's guilds (where the bot is present)
        bot_guilds_resp = await client.get(
            "https://discord.com/api/users/@me/guilds",
            headers={"Authorization": f"Bot {BOT_TOKEN}"}
        )
        bot_guilds = bot_guilds_resp.json()
        bot_guild_ids = {g["id"] for g in bot_guilds}
        
        # Filter guilds where bot is present and user has admin/owner permissions
        filtered = []
        for g in user_guilds:
            if g["id"] not in bot_guild_ids:
                continue
            
            permissions = int(g.get("permissions", 0))
            is_owner = g.get("owner", False)
            is_admin = (permissions & 0x8) == 0x8   # Administrator permission bit
            
            if is_owner or is_admin:
                filtered.append(g)
        
        return filtered
