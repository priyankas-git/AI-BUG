# Ownership: Pavan (API + Static Analysis + Database)
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.analysis import ProjectResponse

router = APIRouter()

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects():
    """
    GET /api/projects
    Return project information.
    """
    # TODO: Fetch list of projects from database
    raise HTTPException(status_code=501, detail="Not Implemented")
