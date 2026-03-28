from fastapi import APIRouter, Query
from app.models.doubt import Doubt

print("ROUTES FILE LOADED") 

router = APIRouter()

doubts_storage = []


@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt):
    doubts_storage.append(doubt.dict())
    return {"message": "Doubt received", "data": doubt}


@router.get("/doubts")
def get_doubts(
    sort: str = Query(None),
    search: str = Query(None),
    limit: int = Query(None)
):
    print("GET /doubts called")  # ✅ now it will run

    result = doubts_storage

   
    if search:
        result = [d for d in result if search.lower() in d["title"].lower()]

    if sort == "upvotes":
        result = sorted(result, key=lambda x: x.get("upvotes", 0), reverse=True)

    
    if limit:
        result = result[:limit]

    return {"doubts": result}