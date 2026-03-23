from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.doubt import Doubt
from app.models.db_models import DoubtModel
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@router.get("/doubts")
def get_doubts(db: Session = Depends(get_db)):
    doubts = db.query(DoubtModel).all()
    return {"doubts": doubts}

@router.post("/doubts/{doubt_id}/upvote")
def upvote_doubt(doubt_id: int, db: Session = Depends(get_db)):
    doubt = db.query(DoubtModel).filter(DoubtModel.id == doubt_id).first()
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")
    doubt.upvotes += 1
    db.commit()
    db.refresh(doubt)
    return {"message": "Upvoted", "data": doubt}

@router.get("/doubts/{doubt_id}")
def get_doubt_by_id(doubt_id: int, db: Session = Depends(get_db)):
    doubt = db.query(DoubtModel).filter(DoubtModel.id == doubt_id).first()
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")
    return {"doubt": doubt}

@router.delete("/doubts/{doubt_id}")
def delete_doubt(doubt_id: int, db: Session = Depends(get_db)):
    doubt = db.query(DoubtModel).filter(DoubtModel.id == doubt_id).first()
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")
    db.delete(doubt)
    db.commit()
    return {"message": "Doubt deleted"}