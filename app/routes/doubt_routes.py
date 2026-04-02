from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models.doubt import Doubt
from app.models.db_models import DoubtModel, Vote
from app.database import SessionLocal
from datetime import datetime

#  IMPORT THE AI ENGINE AND FILTER
from app.services.ai_engine import find_cluster_for_doubt
from app.services.content_filter import filter_doubts

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ SUBMIT DOUBT (AI INTEGRATED) ------------------

@router.post("/submit-doubt")
def submit_doubt(doubt: Doubt, db: Session = Depends(get_db)):
    if not doubt.title.strip() or not doubt.description.strip():
        raise HTTPException(status_code=400, detail="Title and description cannot be empty")

    # 1. Get all existing doubts from the DB
    existing_doubts = db.query(DoubtModel).all()

    # 2. Ask the AI for a cluster_id based on the description
    assigned_cluster_id = find_cluster_for_doubt(doubt.description, existing_doubts)

    # 3. Save to database with the AI cluster_id
    new_doubt = DoubtModel(
        title=doubt.title,
        description=doubt.description,
        submitted_at=str(datetime.now()),
        upvotes=0,
        cluster_id=assigned_cluster_id #  AI Generated ID
    )

    db.add(new_doubt)
    db.commit()
    db.refresh(new_doubt)

    return {"message": "Doubt received and clustered", "data": new_doubt}


# ------------------ GET ALL DOUBTS ------------------

@router.get("/doubts")
def get_doubts(
    search: str = Query(None),
    sort: str = Query(None),
    limit: int = Query(None),
    db: Session = Depends(get_db)
):
    doubts = db.query(DoubtModel).all()

    # Apply filter service
    filtered = filter_doubts(doubts, search, sort, limit)

    result = []
    for d in filtered:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "submitted_at": d.submitted_at,
            "upvotes": d.upvotes,
            "cluster_id": d.cluster_id #  Added this so Frontend can build UI groups
        })

    return {"doubts": result}


# ------------------ UPVOTE (FIXED) ------------------

@router.post("/doubts/{doubt_id}/upvote")
def upvote_doubt(doubt_id: int, db: Session = Depends(get_db)):

    #  TEMP USER (replace later with login system)
    user_id = "temp_user"

    # check if already voted
    existing_vote = db.query(Vote).filter_by(
        doubt_id=doubt_id,
        user_id=user_id
    ).first()

    if existing_vote:
        return {"message": "Already voted"}

    # find doubt
    doubt = db.query(DoubtModel).filter(DoubtModel.id == doubt_id).first()
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    # create vote
    vote = Vote(doubt_id=doubt_id, user_id=user_id)
    db.add(vote)

    # increment upvote
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
    doubt = db.query(DoubtModel).filter(DoubtModel.id == doubt_id).first()

    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    return {"doubt": doubt}


# ------------------ DELETE DOUBT ------------------

@router.delete("/doubts/{doubt_id}")
def delete_doubt(doubt_id: int, db: Session = Depends(get_db)):
    doubt = db.query(DoubtModel).filter(DoubtModel.id == doubt_id).first()

    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    db.delete(doubt)
    db.commit()

    return {"message": "Doubt deleted"}