# Ownership: Pavan (API + Static Analysis + Database)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.project import Project
from schemas.analysis import ProjectResponse

router = APIRouter()

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    """
    GET /api/projects
    Return list of all registered projects from SQLite.
    """
    projects = db.query(Project).all()
    return projects
