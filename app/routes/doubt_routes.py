from fastapi import APIRouter, HTTPException
from app.models.doubt import Doubt

router = APIRouter()
doubts_storage = []

@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt):
    if not doubt.title.strip() or not doubt.description.strip():
        raise HTTPException(status_code=400, detail="Title and description cannot be empty")
    doubts_storage.append(doubt.dict())
    return {"message": "Doubt received", "data": doubt}

@router.get("/doubts")
def get_doubts():
    return {"doubts": doubts_storage}