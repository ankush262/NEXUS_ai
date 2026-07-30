# 🚀 NEXUS AI Copilot Engine (Backend API)

NEXUS is an AI-powered Research & Innovation Copilot built with **FastAPI** and **Google Gemini**. It uses a **Live Search-Augmented Generation (RAG)** pipeline to harvest real-time academic papers, patents, GitHub repositories, and web research across multi-source search engines, synthesizing structured 6-section project reports and executable roadmaps.

---

## ✨ Features

* **Multi-Source RAG Harvester:** Pulls real-time data across Google Scholar, IEEE Xplore, Wiley/Crossref, GitHub, Tavily Web Search, and Google News.
* **Context-Aware Project Chat:** Interactive AI mentor route (`/projects/{id}/chat`) that holds full context of generated project reports.
* **Live SSE Progress Streaming:** Real-time status updates pushed directly to the UI via Server-Sent Events during research execution.
* **Document & Roadmap Exports:** One-click automated PDF report generation (`ReportLab`) and `.ics` iCalendar export (`icalendar`) for milestone scheduling.
* **SQLite Persistence:** Built-in persistence for project histories, task milestones, and legal/compliance flags via `SQLModel`.
* **Instant UI Demo Mode:** Dedicated `/demo-hub` mock route for instant frontend prototyping without API latency or rate limits.

---

## 🛠️ Tech Stack

* **Language & Framework:** Python 3.12+, FastAPI, Uvicorn
* **Database & ORM:** SQLite, SQLModel
* **AI Engine:** Google Gemini (`gemini-3.6-flash`)
* **Live RAG Sources:** Google Scholar (`scholarly`), IEEE Xplore API, Crossref API, GitHub API (`PyGithub`), Tavily AI Search API, Google News API
* **Export & Stream Utilities:** `sse-starlette` (SSE), `reportlab` (PDF generation), `icalendar` (.ics Export)
* **Automation:** Golang (`setup.go`)

---

## 📂 Project Directory Structure

```text
E:\Nexus_AI\backend/
├── .env                        # Environment variables (API Keys)
├── README.md                   # Complete documentation
├── setup.go                    # Automated Golang setup script
└── app/
    ├── main.py                 # FastAPI application entry point & route registration
    ├── api/                    # API Route Controllers
    │   ├── hub.py              # Main report generation, mock hub, & chat endpoints
    │   ├── stream.py           # Server-Sent Events (SSE) live research stream
    │   ├── calendar.py         # .ics calendar roadmap export route
    │   ├── export.py           # ReportLab PDF generation route
    │   └── notifications.py    # Compliance flags & project alerts route
    ├── core/                   # Business Logic & Scrapers
    │   ├── academic_engine.py  # Multi-source live RAG scraper engine
    │   └── hub_generator.py    # Gemini prompt engineering & JSON synthesis engine
    └── db/                     # Database Engine & Schemas
        ├── database.py         # SQLite connection & session management
        └── models.py           # SQLModel schemas (Project, Milestone)

# 🛠️ NEXUS AI Copilot Engine: Manual Setup Guide

This guide covers the manual setup process for configuring and running the NEXUS FastAPI backend using standard Python tools.

---

## 📋 System Prerequisites

Ensure the following tools are installed on your machine before continuing:

* **Python 3.12 or higher** (Verify with `python --version` or `python3 --version`)
* **Git** (Verify with `git --version`)
* **pip** (Python Package Manager)

---

## 🚀 Step-by-Step Manual Setup

### 1. Clone the Repository
Open your terminal and navigate to your working directory, then clone the repository:

```bash
git clone <your-repository-url>
cd backend

2. Create a Python Virtual Environment
Create an isolated virtual environment named .venv in the project root:

Windows:

PowerShell
python -m venv .venv
macOS / Linux:

Bash
python3 -m venv .venv
3. Activate the Virtual Environment
Activate your virtual environment based on your operating system:

Windows (PowerShell):

PowerShell
.\.venv\Scripts\activate
Windows (Command Prompt / cmd):

DOS
.\.venv\Scripts\activate.bat
macOS / Linux:

Bash
source .venv/bin/activate
💡 Tip: Once activated, your terminal prompt will show (.venv) at the beginning of the line.

4. Upgrade pip & Install Dependencies
Ensure pip is up-to-date and install all backend packages:

Bash
pip install --upgrade pip
pip install fastapi uvicorn sqlmodel google-genai scholarly PyGithub tavily-python requests sse-starlette reportlab icalendar
5. Create & Configure the .env File
Create a file named .env in the root folder (E:\Nexus_AI\backend\.env) and insert your API keys:

# Google Gemini API Key (Required for AI Synthesis & Project Chat)
GEMINI_API_KEY="your_gemini_api_key_here"

# GitHub Access Token (Required for open-source repo harvesting)
GITHUB_TOKEN="your_github_token_here"

# Tavily AI Search API Key (Required for live web search and news RAG)
TAVILY_API_KEY="your_tavily_api_key_here"

# IEEE Xplore API Key (Required for academic research papers)
IEEE_API_KEY="your_ieee_api_key_here"

🏃‍♂️ Running the FastAPI Server
Verify that your virtual environment (.venv) is active in your terminal.

Launch the Uvicorn ASGI development server:

Bash
uvicorn app.main:app --reload --port 8000