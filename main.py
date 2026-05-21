# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import gyms, trainers, food, users, crowd
from database.db import engine, Base
from database.seed import seed

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GymSync API",
    description="Backend API for GymSync - Fitness Super App",
    version="1.0.0"
)

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(gyms.router, prefix="/api/gyms", tags=["Gyms"])
app.include_router(trainers.router, prefix="/api/trainers", tags=["Trainers"])
app.include_router(food.router, prefix="/api/food", tags=["Food"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(crowd.router, prefix="/api/crowd", tags=["Crowd"])

@app.get("/")
def root():
    return {
        "app": "GymSync API",
        "version": "1.0.0",
        "status": "running",
        "message": "Welcome to GymSync Backend!"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/seed")
def seed_database():
    """Seed the database with Malappuram gym data"""
    try:
        seed()
        return {"message": "✅ Database seeded successfully with Malappuram gyms!"}
    except Exception as e:
        return {"message": f"Already seeded or error: {str(e)}"}

# Auto seed on startup
@app.on_event("startup")
async def startup_event():
    seed()
