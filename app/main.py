from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
import motor.motor_asyncio
from .database import db
from .routers import auth, guilds, warnings, logs

load_dotenv()

app = FastAPI(title="iSida Dashboard")

# Add session middleware (required for request.session)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-this"))

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    db.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db.database = db.client["iSidaDB"]

@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(guilds.router, prefix="/guilds", tags=["guilds"])
app.include_router(warnings.router, prefix="/warnings", tags=["warnings"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
