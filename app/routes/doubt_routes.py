from fastapi import APIRouter
from app.models.doubt import Doubt

router = APIRouter()

@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt):
    return {
        "message": "Doubt received",
        "data": doubt
    }