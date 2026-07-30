# 🚀 NEXUS — AI-Powered Research & Innovation Copilot

> **Search Less. Solve More. Build Faster.**  
> NEXUS converts raw project ideas into validated research and an actionable, buildable project architecture in minutes.

---

## 🛠️ Tech Stack

* **Frontend:** React (Vite), Tailwind CSS, Lucide Icons, Axios
* **Backend:** Python 3.11+, FastAPI, LangChain, Google Gemini 2.5 API
* **RAG & Search APIs:** ChromaDB (Vector Database), Tavily Search API, ArXiv API, GitHub REST API
* **Database & Export:** SQLite (SQLModel), `icalendar` (.ics Calendar Export)
* **Reminders & Alerts:** In-App Notification Center & Resend Email API

---

## 📁 Repository File Structure

```text
nexus-copilot/
├── README.md                           # Project Documentation
├── docker-compose.yml                  # Container setup for rapid deployment
│
├── backend/                            # FastAPI Backend Engine
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI entry point & CORS middleware
│   │   ├── config.py                  # Environment variables & API key configurations
│   │   │
│   │   ├── api/                        # API Endpoint Routers
│   │   │   ├── __init__.py
│   │   │   ├── validate.py             # POST /api/v1/validate
│   │   │   ├── research.py             # POST /api/v1/research/deep-search
│   │   │   ├── gap_analysis.py         # POST /api/v1/research/gap-analysis
│   │   │   ├── hub.py                  # POST /api/v1/hub/generate
│   │   │   ├── calendar.py             # GET  /api/v1/projects/{id}/calendar (.ics export)
│   │   │   └── notifications.py        # GET  /api/v1/projects/{id}/notifications
│   │   │
│   │   ├── core/                       # Core AI & Search Engines
│   │   │   ├── __init__.py
│   │   │   ├── search_engine.py        # Tavily, ArXiv, and GitHub API integration wrappers
│   │   │   ├── rag_pipeline.py         # ChromaDB vector embedding & document indexing
│   │   │   ├── hub_generator.py        # Gemini 2.5 prompt chains for 6-section structured JSON
│   │   │   └── scheduler.py            # Background job scheduler for email digests (APScheduler)
│   │   │
│   │   ├── db/                         # Data Storage Layer
│   │   │   ├── __init__.py
│   │   │   ├── database.py             # SQLite connection setup
│   │   │   ├── models.py               # SQLModel DB schemas (Projects, Milestones, Alerts)
│   │   │   └── vector_store.py         # ChromaDB instance initialization
│   │   │
│   │   └── schemas/                    # Pydantic Schemas
│   │       ├── request_schemas.py      # Input validation for user prompts
│   │       └── response_schemas.py     # Output formatting for 6-section research output
│   │
│   ├── .env.example                    # Sample environment variables template
│   ├── Dockerfile                      # Backend container definition
│   └── requirements.txt                # Python dependencies
│
└── frontend/                           # React (Vite) Dashboard UI
    ├── public/
    │   └── favicon.ico
    │
    ├── src/
    │   ├── assets/                     # Images, logos, and global SVGs
    │   │
    │   ├── components/                 # React UI Components
    │   │   ├── common/
    │   │   │   ├── Header.jsx          # Top bar with compact prompt input & calendar export
    │   │   │   └── NotificationBell.jsx# In-App deadline alert bell dropdown
    │   │   │
    │   │   ├── dashboard/
    │   │   │   ├── InitialPromptView.jsx # Centered Gemini-style prompt input view
    │   │   │   ├── SidebarNav.jsx      # Left column layout with 6 section tabs
    │   │   │   └── Workspace.jsx       # Right main workspace displaying active section
    │   │   │
    │   │   └── sections/               # The 6 Dedicated Section View Renderers
    │   │       ├── CompetitorsPatents.jsx # Section 1: History, competitors & patent filings
    │   │       ├── MarketResearch.jsx     # Section 2: Target audience & market demand
    │   │       ├── ExistingSolutions.jsx  # Section 3: Existing tools & Gap Finder matrix
    │   │       ├── ResearchPapers.jsx     # Section 4: Academic literature cards
    │   │       ├── IndustryNews.jsx       # Section 5: Recent news & trend articles
    │   │       └── RoadmapBuildHelp.jsx   # Section 6: Architecture, Tech stack & Milestones
    │   │
    │   ├── services/
    │   │   └── api.js                  # Axios client configuration & API call hooks
    │   │
    │   ├── App.jsx                     # Core application view state controller
    │   ├── main.jsx                    # React DOM renderer
    │   └── index.css                   # Tailwind CSS imports
    │
    ├── package.json
    ├── tailwind.config.js              # Tailwind custom colors & animation setup
    └── vite.config.js                  # Vite dev server configuration
