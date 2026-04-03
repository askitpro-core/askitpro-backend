from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.doubt import Doubt
from app.models.db_models import DoubtModel, Vote
from app.database import SessionLocal

#  IMPORT ALL AI TOOLS IN ONE LINE
from app.services.ai_engine import find_cluster_for_doubt, generate_auto_tag, semantic_search
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

    existing_doubts = db.query(DoubtModel).all()

    # 🔥 Ask the AI for the cluster AND the tag
    assigned_cluster_id = find_cluster_for_doubt(doubt.description, existing_doubts)
    assigned_tag = generate_auto_tag(doubt.description) 

    new_doubt = DoubtModel(
        title=doubt.title,
        description=doubt.description,
        submitted_at=str(datetime.now()),
        upvotes=0,
        cluster_id=assigned_cluster_id,
        tag=assigned_tag # 🔥 Save the AI Tag
    )

    db.add(new_doubt)
    db.commit()
    db.refresh(new_doubt)

    return {"message": "Doubt received, clustered, and tagged", "data": new_doubt}

# ------------------ AI SEMANTIC SEARCH ------------------

@router.get("/search")
def search_doubts(query: str = Query(..., description="Type your search here"), db: Session = Depends(get_db)):
    
    # 1. Grab everything from the database
    all_doubts = db.query(DoubtModel).all()
    
    # 2. Feed it into the AI to rank and sort
    ai_results = semantic_search(query, all_doubts)
    
    if not ai_results:
        return {"message": "No conceptually similar doubts found.", "results": []}
        
    return {
        "message": "AI Semantic Search Complete", 
        "search_concept": query,
        "results": ai_results
    }

# ------------------ GET ALL DOUBTS ------------------

@router.get("/doubts")
def get_doubts(
    search: str = Query(None),
    sort: str = Query(None),
    limit: int = Query(None),
    db: Session = Depends(get_db)
):
    doubts = db.query(DoubtModel).all()
    filtered = filter_doubts(doubts, search, sort, limit)

    result = []
    for d in filtered:
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "submitted_at": d.submitted_at,
            "upvotes": d.upvotes,
            "cluster_id": d.cluster_id,
            "tag": d.tag  # YOU ADD IT RIGHT HERE
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