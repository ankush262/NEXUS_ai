from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import get_session
from app.db.models import Project

router = APIRouter()

@router.get("/projects/{project_id}/notifications")
def get_project_notifications(project_id: int, db: Session = Depends(get_session)):
    """Fetches system alerts, license compliance warnings, and roadmap notifications for a specific project."""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return [
        {
            "id": 1,
            "type": "compliance_warning",
            "title": "License Review Recommended",
            "message": "Check dependencies for AGPL or GPL open-source license restrictions before commercial use.",
            "severity": "warning",
            "created_at": "Just now"
        },
        {
            "id": 2,
            "type": "milestone_alert",
            "title": "Phase 1 Milestone",
            "message": "Foundation & API Setup roadmap phase is ready to be exported to your calendar.",
            "severity": "info",
            "created_at": "Just now"
        }
    ]