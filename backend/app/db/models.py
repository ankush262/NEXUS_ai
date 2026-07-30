from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    idea_prompt: str
    generated_data: str  # JSON String storing all 6 sections
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Milestone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    title: str
    phase: int
    days_from_start: int
    is_completed: bool = False

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)