from fastapi import APIRouter, Request, HTTPException
from app.database import db
from bson import ObjectId

router = APIRouter()

@router.get("/{guild_id}")
async def get_transcripts(guild_id: int, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    transcripts_cursor = db.database.ticket_transcripts.find({"guild_id": guild_id}).sort("created_at", -1)
    transcripts = await transcripts_cursor.to_list(length=100)
    for t in transcripts:
        t["_id"] = str(t["_id"])
        if "created_at" in t and hasattr(t["created_at"], "isoformat"):
            t["created_at"] = t["created_at"].isoformat()
    return transcripts

@router.get("/detail/{transcript_id}")
async def get_transcript_detail(transcript_id: str, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        obj_id = ObjectId(transcript_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid transcript ID")
    
    transcript = await db.database.ticket_transcripts.find_one({"_id": obj_id})
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    transcript["_id"] = str(transcript["_id"])
    if "created_at" in transcript and hasattr(transcript["created_at"], "isoformat"):
        transcript["created_at"] = transcript["created_at"].isoformat()
    return transcript
