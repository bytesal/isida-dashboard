from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import os
import httpx
from urllib.parse import quote

router = APIRouter()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
ADMIN_USERS = [int(x.strip()) for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x.strip()]

@router.get("/login")
async def login():
    scope = "identify guilds"
    url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={quote(REDIRECT_URI)}&response_type=code&scope={quote(scope)}"
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str, request: Request):
    async with httpx.AsyncClient() as client:
        token_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
        token_resp = await client.post("https://discord.com/api/oauth2/token", data=token_data)
        token_json = token_resp.json()
        access_token = token_json.get("access_token")
        
        # Fetch user info
        user_resp = await client.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {access_token}"})
        user = user_resp.json()
        
        if user.get("id") and int(user["id"]) not in ADMIN_USERS:
            return {"error": "You are not authorized to access this dashboard."}
        
        # Store user session
        request.session["user"] = user
        request.session["access_token"] = access_token
        return RedirectResponse(url="/dashboard")
