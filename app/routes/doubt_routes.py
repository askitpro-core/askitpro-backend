
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.doubt import Doubt
from app.database import get_db
from app.models.db_models import DoubtDB, Vote
from app.services.content_filter import validate_content, filter_doubts

router = APIRouter()


from app.services.content_filter import validate_content




router = APIRouter()


 main

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
 
def submit_doubt(doubt: Doubt):
    db = next(get_db())

    validate_content(doubt.title)

    if doubt.description:
        validate_content(doubt.description)

    new_doubt = DoubtDB(
        title=doubt.title,
        description=doubt.description
    )

    db.add(new_doubt)
    db.commit()
    db.refresh(new_doubt)

    return {"message": "Doubt received", "data": new_doubt}


def submit_doubt(doubt: Doubt=Body(...)):
    print("......submit doub hit.....")
    validate_content(doubt.title)

    if doubt.description:
        validate_content(doubt.description)

    doubts_storage.append(doubt.dict())

    return {"message": "Doubt received", "data": doubt}


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.doubt import Doubt
from app.models.db_models import DoubtModel, Vote
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ SUBMIT DOUBT ------------------

@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt, db: Session = Depends(get_db)):
    if not doubt.title.strip() or not doubt.description.strip():
        raise HTTPException(status_code=400, detail="Title and description cannot be empty")

    new_doubt = DoubtModel(
        title=doubt.title,
        description=doubt.description,
        submitted_at=str(datetime.now()),
        upvotes=0
    )

    db.add(new_doubt)
    db.commit()
    db.refresh(new_doubt)

    return {"message": "Doubt received", "data": new_doubt}


# ------------------ GET ALL DOUBTS ------------------

from fastapi import Query
from app.services.content_filter import filter_doubts

@router.get("/doubts")

@router.get("/doubts")
def get_doubts(
    search: str = Query(None),
    sort: str = Query(None),
    limit: int = Query(None),
    db: Session = Depends(get_db)
):
    doubts = db.query(DoubtDB).all()

    filtered = filter_doubts(doubts, search, sort, limit)

    result = []
    for d in filtered:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "submitted_at": d.submitted_at,
            "upvotes": d.upvotes
        })

    return {"doubts": result}


# ------------------ UPVOTE ------------------

@router.post("/doubts/{doubt_id}/upvote")
def upvote_doubt(doubt_id: int, db: Session = Depends(get_db)):

    user_id = "temp_user"

    existing_vote = db.query(Vote).filter_by(
        doubt_id=doubt_id,
        user_id=user_id
    ).first()

    if existing_vote:
        return {"message": "Already voted"}

    doubt = db.query(DoubtDB).filter(DoubtDB.id == doubt_id).first()
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    vote = Vote(doubt_id=doubt_id, user_id=user_id)
    db.add(vote)

    doubt.upvotes += 1

    db.commit()
    db.refresh(doubt)

    return {
        "message": "Upvoted",
        "data": {
            "id": doubt.id,
            "upvotes": doubt.upvotes
        }
    }


# ------------------ GET SINGLE DOUBT ------------------

@router.get("/doubts/{doubt_id}")
def get_doubt_by_id(doubt_id: int, db: Session = Depends(get_db)):
    doubt = db.query(DoubtDB).filter(DoubtDB.id == doubt_id).first()

    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    return {"doubt": doubt}


# ------------------ DELETE DOUBT ------------------

@router.delete("/doubts/{doubt_id}")
def delete_doubt(doubt_id: int, db: Session = Depends(get_db)):
    doubt = db.query(DoubtDB).filter(DoubtDB.id == doubt_id).first()

    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    db.delete(doubt)
    db.commit()

    return {"message": "Doubt deleted"}


