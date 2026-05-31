# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import gyms, trainers, food, users, crowd
from database.db import engine, Base
from database.seed import seed
import os

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

# Serve static files (staff panel)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/staff")
def staff_panel():
    """Gym staff crowd update panel"""
    return FileResponse("static/index.html")

@app.post("/seed")
def seed_database():
    try:
        seed()
        return {"message": "✅ Database seeded with Malappuram gyms!"}
    except Exception as e:
        return {"message": f"Already seeded or error: {str(e)}"}

@app.on_event("startup")
async def startup_event():
    try:
        seed()
    except Exception as e:
        print(f"Seed error: {e}")
