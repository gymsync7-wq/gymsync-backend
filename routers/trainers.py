# routers/trainers.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import Trainer

router = APIRouter()

@router.get("/")
def get_trainers(gym_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Trainer).filter(Trainer.is_active == True)
    if gym_id:
        query = query.filter(Trainer.gym_id == gym_id)
    trainers = query.all()
    return {
        "trainers": [
            {
                "id": str(t.id),
                "name": t.name,
                "gymId": str(t.gym_id),
                "specialty": t.specialty,
                "experience": t.experience,
                "pricePerSession": t.price_per_session,
                "rating": t.rating,
                "reviews": t.reviews,
                "bio": t.bio,
                "certifications": t.certifications or [],
                "isOnline": t.is_online,
                "phone": t.phone,
            }
            for t in trainers
        ]
    }
