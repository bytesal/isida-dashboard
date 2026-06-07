from fastapi import APIRouter, HTTPException, Request
import httpx
import os

router = APIRouter()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

@router.get("/guilds/{guild_id}/channels")
async def get_guild_channels(guild_id: int, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://discord.com/api/guilds/{guild_id}/channels", headers={"Authorization": f"Bot {BOT_TOKEN}"})
        return resp.json()

@router.get("/guilds/{guild_id}/roles")
async def get_guild_roles(guild_id: int, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://discord.com/api/guilds/{guild_id}/roles", headers={"Authorization": f"Bot {BOT_TOKEN}"})
        return resp.json()