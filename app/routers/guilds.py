from fastapi import APIRouter, Request, HTTPException
import httpx

router = APIRouter()

@router.get("/")
async def list_guilds(request: Request):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://discord.com/api/users/@me/guilds", headers={"Authorization": f"Bearer {token}"})
        guilds = resp.json()
        # Filter where bot is present (optional)
        return guilds
