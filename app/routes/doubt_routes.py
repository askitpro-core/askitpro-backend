from fastapi import APIRouter
from app.models.doubt import Doubt
from app.database import get_db
from app.models.db_models import DoubtDB
from app.services.content_filter import validate_content

router = APIRouter()


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


@router.get("/doubts")
def get_doubts():
    db = next(get_db())

    doubts = db.query(DoubtDB).all()

    return {"doubts": doubts}