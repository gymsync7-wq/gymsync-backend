# routers/gyms.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database.db import get_db
from models.models import Gym, CrowdLog
import math

router = APIRouter()

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(R * c, 1)

def gym_to_dict(gym, distance=None):
    crowd_pct = round((gym.current_crowd / gym.total_capacity) * 100) if gym.total_capacity > 0 else 0
    if crowd_pct < 40:
        crowd_label = "Quiet"
        crowd_color = "#1DB954"
    elif crowd_pct < 70:
        crowd_label = "Moderate"
        crowd_color = "#F59E0B"
    else:
        crowd_label = "Busy"
        crowd_color = "#EF4444"

    return {
        "id": str(gym.id),
        "name": gym.name,
        "area": gym.area,
        "address": gym.address,
        "city": gym.city,
        "phone": gym.phone,
        "latitude": gym.latitude,
        "longitude": gym.longitude,
        "rating": gym.rating,
        "reviews": gym.reviews,
        "monthlyPrice": gym.monthly_price,
        "dayPassPrice": gym.day_pass_price,
        "openTime": gym.open_time,
        "closeTime": gym.close_time,
        "totalCapacity": gym.total_capacity,
        "currentCount": gym.current_crowd,
        "crowdPercent": crowd_pct,
        "crowdLabel": crowd_label,
        "crowdColor": crowd_color,
        "amenities": gym.amenities or [],
        "isVerified": gym.is_verified,
        "distance": f"{distance} km" if distance else "Nearby",
    }

@router.get("/")
def get_all_gyms(
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    radius: float = Query(50),
    db: Session = Depends(get_db)
):
    gyms = db.query(Gym).filter(Gym.is_active == True).all()
    result = []
    for gym in gyms:
        distance = None
        if lat and lng:
            distance = calculate_distance(lat, lng, gym.latitude, gym.longitude)
            if distance > radius:
                continue
        result.append(gym_to_dict(gym, distance))

    # Sort by distance if provided
    if lat and lng:
        result.sort(key=lambda x: float(x["distance"].replace(" km", "")) if x["distance"] != "Nearby" else 999)

    return {"gyms": result, "total": len(result)}

@router.get("/{gym_id}")
def get_gym(gym_id: int, db: Session = Depends(get_db)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")
    return gym_to_dict(gym)

@router.get("/{gym_id}/crowd")
def get_crowd(gym_id: int, db: Session = Depends(get_db)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")

    crowd_pct = round((gym.current_crowd / gym.total_capacity) * 100) if gym.total_capacity > 0 else 0

    # Generate hourly prediction (mock ML prediction)
    import random
    base = [10, 15, 25, 45, 70, 85, 65, 50, 40, 35, 55, 75]
    prediction = [min(100, max(0, b + random.randint(-10, 10))) for b in base]

    return {
        "gymId": gym_id,
        "currentCount": gym.current_crowd,
        "totalCapacity": gym.total_capacity,
        "crowdPercent": crowd_pct,
        "hourlyPrediction": prediction,
    }

@router.put("/{gym_id}/crowd")
def update_crowd(gym_id: int, count: int, db: Session = Depends(get_db)):
    """Gym staff updates crowd count"""
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")

    gym.current_crowd = min(count, gym.total_capacity)
    db.commit()

    # Log crowd data
    log = CrowdLog(
        gym_id=gym_id,
        count=count,
        capacity_percent=round((count / gym.total_capacity) * 100)
    )
    db.add(log)
    db.commit()

    return {"message": "Crowd updated", "currentCount": gym.current_crowd}

@router.get("/search/{query}")
def search_gyms(query: str, db: Session = Depends(get_db)):
    gyms = db.query(Gym).filter(
        (Gym.name.ilike(f"%{query}%")) |
        (Gym.area.ilike(f"%{query}%")) |
        (Gym.city.ilike(f"%{query}%"))
    ).all()
    return {"gyms": [gym_to_dict(g) for g in gyms]}
