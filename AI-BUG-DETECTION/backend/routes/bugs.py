# Ownership: Pavan (API + Static Analysis + Database)
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.bug import BugResponse

router = APIRouter()

@router.get("/bugs", response_model=List[BugResponse])
def get_bugs():
    """
    GET /api/bugs
    Return detected bugs.
    """
    # TODO: Fetch bugs from SQLite database
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/bugs/{bug_id}", response_model=BugResponse)
def get_bug_by_id(bug_id: str):
    """
    GET /api/bugs/{bug_id}
    Return detailed information for a bug.
    """
    # TODO: Fetch bug by ID from database
    raise HTTPException(status_code=501, detail="Not Implemented")
