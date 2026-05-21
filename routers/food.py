# routers/food.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import FoodItem

router = APIRouter()

@router.get("/")
def get_food(category: str = None, db: Session = Depends(get_db)):
    query = db.query(FoodItem).filter(FoodItem.is_available == True)
    if category and category != "All":
        query = query.filter(FoodItem.category == category)
    items = query.all()
    return {
        "items": [
            {
                "id": str(f.id),
                "name": f.name,
                "restaurant": f.restaurant,
                "price": f.price,
                "calories": f.calories,
                "protein": f.protein,
                "carbs": f.carbs,
                "fat": f.fat,
                "category": f.category,
                "prepTime": f.prep_time,
                "tags": f.tags or [],
                "area": f.area,
            }
            for f in items
        ]
    }
