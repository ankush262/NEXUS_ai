import os
from sqlmodel import SQLModel, create_engine, Session
from app.db.models import Project, Milestone, Notification 

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nexus.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session