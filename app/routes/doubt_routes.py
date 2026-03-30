from fastapi import APIRouter, Query,Body
from app.models.doubt import Doubt
from app.services.content_filter import validate_content

print("ROUTES FILE LOADED") 
# filtering implemented

router = APIRouter()

doubts_storage = []

@router.get("/doubts")
def get_doubts(
    sort: str = Query(None),
    search: str = Query(None),
    limit: int = Query(None)
):
    print("GET /doubts called") 

    result = doubts_storage

   
    if search:
        result = [d for d in result if search.lower() in d["title"].lower()]

    if sort == "upvotes":
        result = sorted(result, key=lambda x: x.get("upvotes", 0), reverse=True)

    
    if limit:
        result = result[:limit]

    return {"doubts": result}
@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt=Body(...)):
    print("......submit doub hit.....")
    validate_content(doubt.title)

    if doubt.description:
        validate_content(doubt.description)

    doubts_storage.append(doubt.dict())

    return {"message": "Doubt received", "data": doubt}