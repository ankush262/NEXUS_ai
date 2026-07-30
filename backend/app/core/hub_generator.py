import json
import os
from google import genai
from google.genai import types

def synthesize_nexus_report(idea: str, extracted_context: list) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY missing in environment variables")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are NEXUS, an AI Research & Innovation Copilot.
    Student Project Idea: "{idea}"
    Live Harvested Sources: {json.dumps(extracted_context)}

    STRICT INSTRUCTIONS FOR SOURCE INTEGRATION:
    1. Populate 'research_papers' using the Google Scholar, IEEE, and Wiley items provided in the harvested sources. Keep exact URLs where available.
    2. Populate 'news_articles' using the Google News items provided in the harvested sources.
    3. Populate 'competitors_patents' using the GitHub repositories and Tavily search items provided.
    4. In 'legal_and_compliance', evaluate any GPL or open-source license risks found in the GitHub repos, as well as GDPR/privacy risks.

    Generate a structured JSON response matching this schema EXACTLY:

    {{
      "summary": {{
        "project_title": "Descriptive short title",
        "executive_summary": "3-4 sentence overview of problem, solution, and viability.",
        "viability_score": "e.g., 8.8/10",
        "key_innovation": "The unique value proposition"
      }},
      "legal_and_compliance": {{
        "open_source_license_warnings": "Specific licensing risks based on GitHub repos or code dependencies.",
        "data_privacy_flags": "GDPR, HIPAA, or student privacy considerations.",
        "disclaimer": "AI recommendations; legal compliance should be independently verified."
      }},
      "sections": {{
        "competitors_patents": {{
          "title": "Competitors & Patents",
          "competitors": [{{"name": "Comp/Repo Name", "description": "Short summary", "url": "URL"}}],
          "patents": [{{"title": "Patent Title or Related Tech", "summary": "Abstract"}}]
        }},
        "market_research": {{
          "title": "Market Research",
          "target_audience": "Who uses this",
          "market_demand": "Current industry demand"
        }},
        "existing_solutions": {{
          "title": "Existing Solutions & Gaps",
          "current_tools": [{{"name": "Tool", "limitation": "Drawback"}}],
          "gap_analysis": "Key missing feature in existing solutions"
        }},
        "research_papers": {{
          "title": "Academic Research Papers",
          "papers": [{{"title": "Title", "source": "Google Scholar/IEEE/Wiley", "url": "URL", "takeaway": "Key takeaway"}}]
        }},
        "news_articles": {{
          "title": "Industry News & Articles",
          "articles": [{{"headline": "Title", "source": "Google News", "url": "URL"}}]
        }},
        "roadmap_and_help": {{
          "title": "Roadmap & Build Help",
          "architecture_summary": "System architecture pipeline",
          "tech_stack": ["React", "FastAPI", "SQLite", "Gemini API"],
          "roadmap": [
            {{"phase": 1, "title": "Foundation & API Setup", "days_required": 2, "tasks": ["Task 1", "Task 2"]}}
          ]
        }}
      }}
    }}

    Return STRICTLY valid JSON.
    """

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )

    return json.loads(response.text)