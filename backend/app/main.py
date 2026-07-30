from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db

# 1. Use explicit imports to prevent naming conflicts (especially with 'calendar')
from app.api.hub import router as hub_router
from app.api.calendar import router as calendar_router
from app.api.notifications import router as notifications_router
from app.api.stream import router as stream_router
from app.api.export import router as export_router

# 2. Initialize FastAPI Application
app = FastAPI(
    title="NEXUS AI Copilot Engine",
    description="Backend API for AI-Powered Research & Innovation Copilot",
    version="1.0.0"
)

# 3. Enable CORS so React Frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Initialize SQLite Database Tables on Startup
@app.on_event("startup")
def on_startup():
    init_db()

# 5. Include ALL 5 Routers
app.include_router(hub_router, prefix="/api/v1", tags=["Project HUB"])
app.include_router(calendar_router, prefix="/api/v1", tags=["Calendar Export"])
app.include_router(notifications_router, prefix="/api/v1", tags=["Notifications"])
app.include_router(stream_router, prefix="/api/v1", tags=["Live Progress Stream"])
app.include_router(export_router, prefix="/api/v1", tags=["PDF Export"])

# 6. Root Healthcheck Route
@app.get("/", tags=["default"])
def root():
    return {"status": "online", "message": "NEXUS Core Engine is operational!"}