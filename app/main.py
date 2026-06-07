from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import motor.motor_asyncio
from .database import db
from .routers import auth, guilds, warnings, logs

load_dotenv()

app = FastAPI(title="iSida Dashboard")

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
    return templates.TemplateResponse("index.html", {"request": request})
