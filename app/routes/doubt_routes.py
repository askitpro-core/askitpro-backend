from fastapi import APIRouter, HTTPException
from app.models.doubt import Doubt

router = APIRouter()
doubts_storage = []
counter = 0

@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt):
    global counter
    if not doubt.title.strip() or not doubt.description.strip():
        raise HTTPException(status_code=400, detail="Title and description cannot be empty")
    counter += 1
    doubt_entry = doubt.dict()
    doubt_entry["id"] = counter
    doubt_entry["upvotes"] = 0
    doubts_storage.append(doubt_entry)
    return {"message": "Doubt received", "data": doubt_entry}

@router.get("/doubts")
def get_doubts():
    return {"doubts": doubts_storage}

@router.post("/doubts/{doubt_id}/upvote")
def upvote_doubt(doubt_id: int):
    for doubt in doubts_storage:
        if doubt["id"] == doubt_id:
            doubt["upvotes"] += 1
            return {"message": "Upvoted", "data": doubt}
    raise HTTPException(status_code=404, detail="Doubt not found")