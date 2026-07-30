import asyncio
import json
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse
from sqlmodel import Session
from app.db.database import get_session
from app.core.academic_engine import gather_all_academic_and_web_data
from app.core.hub_generator import synthesize_nexus_report
from app.db.models import Project, Milestone

router = APIRouter()

async def nexus_generator_stream(request: Request, idea: str, db: Session):
    """Generator that yields live SSE updates to the frontend."""
    try:
        # Step 1: Notify frontend that harvesting has started
        yield {"event": "status", "data": "Starting NEXUS AI Engine..."}
        await asyncio.sleep(0.5)

        yield {"event": "status", "data": "Harvesting live data from Google Scholar & IEEE Xplore..."}
        # Run the heavy scraper in a background thread so we don't block the async loop
        extracted_data = await asyncio.to_thread(gather_all_academic_and_web_data, idea)

        # Step 2: Notify frontend about AI synthesis
        yield {"event": "status", "data": f"Harvest complete. Found {len(extracted_data)} sources. Synthesizing report with Gemini..."}
        report_json = await asyncio.to_thread(synthesize_nexus_report, idea, extracted_data)

        # Step 3: Save to Database
        yield {"event": "status", "data": "Finalizing architecture and saving to database..."}
        
        project = Project(
            title=report_json.get("summary", {}).get("project_title", idea[:30]),
            idea_prompt=idea,
            generated_data=json.dumps(report_json)
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        # Step 4: Send the final success event with the project ID
        yield {"event": "complete", "data": json.dumps({"project_id": project.id})}

    except Exception as e:
        yield {"event": "error", "data": str(e)}

@router.get("/generate-stream")
async def generate_project_stream(request: Request, idea: str, db: Session = Depends(get_session)):
    """SSE Endpoint. The frontend will connect to this URL via `new EventSource()`."""
    return EventSourceResponse(nexus_generator_stream(request, idea, db))