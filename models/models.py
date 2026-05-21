# models/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from database.db import Base

class Gym(Base):
    __tablename__ = "gyms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    area = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, default="Malappuram")
    state = Column(String, default="Kerala")
    phone = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rating = Column(Float, default=4.0)
    reviews = Column(Integer, default=0)
    monthly_price = Column(Integer, nullable=False)
    day_pass_price = Column(Integer, nullable=False)
    open_time = Column(String, default="6:00 AM")
    close_time = Column(String, default="10:00 PM")
    total_capacity = Column(Integer, default=50)
    current_crowd = Column(Integer, default=0)
    amenities = Column(JSON, default=[])
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    gym_id = Column(Integer, nullable=False)
    specialty = Column(String, nullable=False)
    experience = Column(String)
    price_per_session = Column(Integer, nullable=False)
    rating = Column(Float, default=4.0)
    reviews = Column(Integer, default=0)
    bio = Column(Text)
    certifications = Column(JSON, default=[])
    is_online = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    phone = Column(String)

class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    restaurant = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    calories = Column(Integer)
    protein = Column(Integer)
    carbs = Column(Integer)
    fat = Column(Integer)
    category = Column(String)
    prep_time = Column(String)
    tags = Column(JSON, default=[])
    is_available = Column(Boolean, default=True)
    area = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, nullable=False)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    goal = Column(String)
    fitness_level = Column(String)
    sync_coins = Column(Integer, default=100)
    streak = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class CrowdLog(Base):
    __tablename__ = "crowd_logs"

    id = Column(Integer, primary_key=True, index=True)
    gym_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    capacity_percent = Column(Float)
    logged_at = Column(DateTime, server_default=func.now())

class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    gym_id = Column(Integer, nullable=False)
    plan_type = Column(String)  # day / monthly
    amount_paid = Column(Integer)
    razorpay_payment_id = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)
