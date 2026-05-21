# routers/crowd.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import CrowdLog

router = APIRouter()

@router.get("/{gym_id}/history")
def get_crowd_history(gym_id: int, db: Session = Depends(get_db)):
    logs = db.query(CrowdLog).filter(
        CrowdLog.gym_id == gym_id
    ).order_by(CrowdLog.logged_at.desc()).limit(24).all()
    return {
        "history": [
            {
                "count": log.count,
                "capacityPercent": log.capacity_percent,
                "loggedAt": str(log.logged_at),
            }
            for log in logs
        ]
    }
