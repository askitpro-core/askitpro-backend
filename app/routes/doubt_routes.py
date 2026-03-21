from fastapi import APIRouter
from app.models.doubt import Doubt

router = APIRouter()
doubts_storage = []

@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt):
    doubts_storage.append(doubt.dict())
    return {"message": "Doubt received", "data": doubt}

@router.get("/doubts")
def get_doubts():
    return {"doubts": doubts_storage}
