from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
import motor.motor_asyncio
from .database import db
from .routers import auth, guilds, warnings, logs, verification, discord, transcripts

load_dotenv()

app = FastAPI(title="iSida Dashboard")

# Session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "fallback-secret-key-change-this"))

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not set")
    db.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    db.database = db.client["iSidaDB"]

@app.on_event("shutdown")
async def shutdown_db_client():
    if db.client:
        db.client.close()

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ========== HTML PAGE ROUTES ==========
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/warnings/{guild_id}", response_class=HTMLResponse)
async def warnings_page(request: Request, guild_id: int):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("warnings.html", {"request": request, "guild_id": guild_id})

@app.get("/logs/{guild_id}", response_class=HTMLResponse)
async def logs_page(request: Request, guild_id: int):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("logs.html", {"request": request, "guild_id": guild_id})

@app.get("/verification/{guild_id}", response_class=HTMLResponse)
async def verification_page(request: Request, guild_id: int):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("verification.html", {"request": request, "guild_id": guild_id})

@app.get("/transcripts/{guild_id}", response_class=HTMLResponse)
async def transcripts_page(request: Request, guild_id: int):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("transcripts.html", {"request": request, "guild_id": guild_id})

# ========== API ROUTES ==========
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(guilds.router, prefix="/api/guilds", tags=["guilds"])
app.include_router(warnings.router, prefix="/api/warnings", tags=["warnings"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(verification.router, prefix="/api/verification", tags=["verification"])
app.include_router(discord.router, prefix="/api/discord", tags=["discord"])
app.include_router(transcripts.router, prefix="/api/transcripts", tags=["transcripts"])
