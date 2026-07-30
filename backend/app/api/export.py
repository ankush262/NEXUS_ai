import json
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from app.db.database import get_session
from app.db.models import Project

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

router = APIRouter()

@router.get("/projects/{project_id}/export/pdf")
def export_project_pdf(project_id: int, db: Session = Depends(get_session)):
    """Generates a downloadable PDF report of the saved project."""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    data = json.loads(project.generated_data)
    styles = getSampleStyleSheet()
    
    # Create an in-memory byte stream for the PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # 1. Title Page
    title = data.get("summary", {}).get("project_title", "NEXUS Project Report")
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 12))

    # 2. Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    summary_text = data.get("summary", {}).get("executive_summary", "No summary available.")
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # 3. Market Research
    story.append(Paragraph("Market Research", styles['Heading2']))
    market = data.get("sections", {}).get("market_research", {})
    story.append(Paragraph(f"<b>Target Audience:</b> {market.get('target_audience', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Market Demand:</b> {market.get('market_demand', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Build the PDF
    doc.build(story)
    
    # Reset buffer position to the beginning so FastAPI can stream it
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=nexus_project_{project_id}.pdf"}
    )