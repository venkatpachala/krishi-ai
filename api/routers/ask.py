from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Session

from ..deps import get_db
from ..rag import search
from ..llm_client import generate_answer
from ..models import QueryLog
from ..grounding import get_weather

router = APIRouter(prefix="/api", tags=["ask"])

class AskRequest(BaseModel):
    query: str
    crop: Optional[str] = None
    stage: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    image: Optional[str] = None

@router.post("/ask")
async def ask(req: AskRequest, db: Session = Depends(get_db)):
    docs = search(db, req.query)
    context = [d.content for d in docs]
    if req.lat and req.lon:
        context.append(get_weather(req.lat, req.lon))
    result = generate_answer(req.query, context, image=req.image)
    qlog = QueryLog(query=req.query, answer=str(result), confidence=result.get("confidence"), lat=req.lat, lon=req.lon)
    db.add(qlog)
    db.commit()
    return result
