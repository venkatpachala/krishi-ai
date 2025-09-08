from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import math

from ..deps import get_db
from ..models import Officer, QueryLog

router = APIRouter(prefix="/api", tags=["escalate"])

class EscalateRequest(BaseModel):
    query_id: int
    notes: Optional[str] = None

class OfficerOut(BaseModel):
    name: str
    phone: str
    distance_km: float

@router.post("/escalate", response_model=List[OfficerOut])
def escalate(req: EscalateRequest, db: Session = Depends(get_db)):
    q = db.get(QueryLog, req.query_id)
    if not q:
        return []
    officers = db.query(Officer).all()
    def dist(o):
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [q.lat, q.lon, o.lat, o.lon])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R*c
    results = [OfficerOut(name=o.name, phone=o.phone, distance_km=dist(o)) for o in officers]
    results.sort(key=lambda x: x.distance_km)
    return results[:3]
