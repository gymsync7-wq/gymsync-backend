# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import User
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    firebase_uid: str
    name: str = None
    email: str = None
    phone: str = None
    goal: str = None
    fitness_level: str = None

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.firebase_uid == user.firebase_uid).first()
    if existing:
        return {"user": user_to_dict(existing), "created": False}
    new_user = User(**user.dict(), sync_coins=100)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user": user_to_dict(new_user), "created": True}

@router.get("/{firebase_uid}")
def get_user(firebase_uid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_dict(user)

@router.put("/{firebase_uid}/coins")
def add_coins(firebase_uid: str, amount: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.sync_coins += amount
    db.commit()
    return {"syncCoins": user.sync_coins}

def user_to_dict(user):
    return {
        "id": user.id,
        "firebaseUid": user.firebase_uid,
        "name": user.name,
        "email": user.email,
        "goal": user.goal,
        "fitnessLevel": user.fitness_level,
        "syncCoins": user.sync_coins,
        "streak": user.streak,
    }
