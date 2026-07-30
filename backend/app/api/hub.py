from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
import json

from app.db.database import get_session
from app.db.models import Project, Milestone
from app.core.academic_engine import gather_all_academic_and_web_data
from app.core.hub_generator import synthesize_nexus_report

router = APIRouter()

class IdeaRequest(BaseModel):
    idea: str
class IdeaRequest(BaseModel):
    idea: str

# ADD THIS:
class ChatRequest(BaseModel):
    message: str


@router.get("/demo-hub")
def get_demo_project_hub():
    """Instant endpoint for frontend dev to test UI layout without API delays or AI rate limits."""
    return {
        "project_id": 999,
        "payload": {
            "summary": {
                "project_title": "AI Hostel Food Waste Reducer",
                "executive_summary": "An IoT and Computer Vision system designed to predict food prep quantities in college mess halls, reducing waste by up to 35%.",
                "viability_score": "8.9/10",
                "key_innovation": "Predictive Mess Attendance Modeling via Student Schedule Analysis"
            },
            "legal_and_compliance": {
                "open_source_license_warnings": "Uses AGPL-3.0 computer vision libraries; commercial redistribution requires open-sourcing.",
                "data_privacy_flags": "Captures facial biometric data in cafeterias—requires GDPR/DPDP consent forms.",
                "disclaimer": "AI recommendations; legal compliance should be independently verified."
            },
            "sections": {
                "competitors_patents": {
                    "title": "Competitors & Patents",
                    "competitors": [{"name": "Winnow Vision", "description": "AI commercial kitchen bin tracker", "url": "https://www.winnowsolutions.com"}],
                    "patents": [{"title": "US10482491B2", "summary": "Automated food waste monitoring apparatus"}]
                },
                "market_research": {
                    "title": "Market Research",
                    "target_audience": "University Mess Committees, Hotel Catering Operations",
                    "market_demand": "High demand driven by institutional sustainability goals."
                },
                "existing_solutions": {
                    "title": "Existing Solutions & Gaps",
                    "current_tools": [{"name": "Manual Log Books", "limitation": "High human error, no predictive capabilities"}],
                    "gap_analysis": "Lack of real-time attendance integration with academic timetables."
                },
                "research_papers": {
                    "title": "Academic Research Papers",
                    "papers": [{"title": "Deep Learning for Food Quantity Estimation", "source": "IEEE Xplore", "url": "https://ieeexplore.ieee.org", "takeaway": "CNN models achieve 92% accuracy in portion size prediction."}]
                },
                "news_articles": {
                    "title": "Industry News & Articles",
                    "articles": [{"headline": "How Universities Are Cutting Food Waste With AI", "source": "Google News", "url": "https://news.google.com"}]
                },
                "roadmap_and_help": {
                    "title": "Roadmap & Build Help",
                    "architecture_summary": "Camera Stream -> OpenCV Preprocessing -> FastSAM Model -> FastAPI Server -> SQLite",
                    "tech_stack": ["React", "FastAPI", "SQLite", "OpenCV", "Gemini API"],
                    "roadmap": [
                        {"phase": 1, "title": "Data Collection & Camera Setup", "days_required": 3, "tasks": ["Install camera above waste tray", "Collect 500 training images"]}
                    ]
                }
            }
        }
    }


@router.post("/generate-hub")
def generate_project_hub(req: IdeaRequest, db: Session = Depends(get_session)):
    """Harvests live research across multi-source engines, synthesizes a 6-section report via Gemini, and saves to DB."""
    try:
        # 1. Harvest multi-source research across Scholar, IEEE, Wiley, GitHub, Tavily, News
        extracted_data = gather_all_academic_and_web_data(req.idea)
        
        # 2. Synthesize structured report via Gemini 3.6 Flash
        report_json = synthesize_nexus_report(req.idea, extracted_data)
        
        # 3. Save Project to SQLite Database
        project = Project(
            title=report_json.get("summary", {}).get("project_title", req.idea[:30]),
            idea_prompt=req.idea,
            generated_data=json.dumps(report_json)
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # 4. Save Roadmap Milestones for Calendar Export (.ics)
        roadmap = report_json.get("sections", {}).get("roadmap_and_help", {}).get("roadmap", [])
        start_day = 1
        for phase in roadmap:
            m = Milestone(
                project_id=project.id,
                phase=phase.get("phase", 1),
                title=phase.get("title", "Phase"),
                days_from_start=start_day
            )
            start_day += phase.get("days_required", 2)
            db.add(m)
            
        db.commit()
        return {"project_id": project.id, "payload": report_json}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "HUB_GENERATION_FAILED",
                "message": "Failed to generate project hub.",
                "details": str(e)
            }
        )


@router.get("/projects")
def list_all_projects(db: Session = Depends(get_session)):
    """Fetches all generated projects for sidebar/history navigation."""
    try:
        projects = db.exec(select(Project).order_by(Project.created_at.desc())).all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "idea_prompt": p.idea_prompt,
                "created_at": p.created_at
            }
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}")
def get_project_by_id(project_id: int, db: Session = Depends(get_session)):
    """Fetches a single saved project by ID."""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project.id,
        "payload": json.loads(project.generated_data)
    }
# Don't forget to import the new function at the top of the file!
# from app.core.hub_generator import synthesize_nexus_report, chat_with_nexus

@router.post("/projects/{project_id}/chat")
def project_chat(project_id: int, req: ChatRequest, db: Session = Depends(get_session)):
    """Interactive chat endpoint to ask follow-up questions about a generated project."""
    # 1. Fetch the saved project from the database
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    from app.core.hub_generator import chat_with_nexus
    
    try:
        # 2. Feed the saved JSON and the user's message to Gemini
        ai_reply = chat_with_nexus(project.generated_data, req.message)
        
        # 3. Return the AI's response
        return {
            "project_id": project_id,
            "user_message": req.message,
            "ai_reply": ai_reply
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "CHAT_FAILED",
                "message": "Failed to communicate with NEXUS AI.",
                "details": str(e)
            }
        )