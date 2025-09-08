from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from ..deps import get_db
from ..models import Feedback

router = APIRouter(prefix="/api", tags=["feedback"])

class FeedbackRequest(BaseModel):
    query_id: int
    rating: int
    comment: Optional[str] = None

@router.post("/feedback")
def add_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    fb = Feedback(query_id=req.query_id, rating=req.rating, comment=req.comment)
    db.add(fb)
    db.commit()
    return {"status": "ok"}
