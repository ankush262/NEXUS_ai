from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from app.db.database import get_session
from app.db.models import Milestone

router = APIRouter()

@router.get("/projects/{project_id}/calendar")
def export_calendar(project_id: int, db: Session = Depends(get_session)):
    milestones = db.exec(select(Milestone).where(Milestone.project_id == project_id)).all()
    if not milestones:
        raise HTTPException(status_code=404, detail="No milestones found for this project ID")

    cal = Calendar()
    cal.add('prodid', '-//NEXUS Copilot Roadmap//nexus.ai//')
    cal.add('version', '2.0')

    now = datetime.now()
    for m in milestones:
        event = Event()
        event.add('summary', f"NEXUS Phase {m.phase}: {m.title}")
        start_date = now + timedelta(days=m.days_from_start)
        event.add('dtstart', start_date.date())
        event.add('dtend', (start_date + timedelta(days=1)).date())
        cal.add_component(event)

    return Response(
        content=cal.to_ical(),
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=nexus_project_{project_id}.ics"}
    )