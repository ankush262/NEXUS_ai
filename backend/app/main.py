from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.api import hub

# 1. Initialize FastAPI Application
app = FastAPI(
    title="NEXUS AI Copilot Engine",
    description="Backend API for AI-Powered Research & Innovation Copilot",
    version="1.0.0"
)

# 2. Enable CORS so React Frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize SQLite Database Tables on Startup
@app.on_event("startup")
def on_startup():
    init_db()

# 4. Include Routers
app.include_router(hub.router, prefix="/api/v1", tags=["Project HUB"])

# 5. Root Healthcheck Route
@app.get("/")
def root():
    return {"status": "online", "message": "NEXUS Core Engine is operational!"}