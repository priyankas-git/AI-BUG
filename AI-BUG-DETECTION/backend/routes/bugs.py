# Ownership: Pavan (API + Static Analysis + Database)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.bug import Bug
from schemas.bug import BugResponse

router = APIRouter()

@router.get("/bugs", response_model=List[BugResponse])
def get_bugs(db: Session = Depends(get_db)):
    """
    GET /api/bugs
    Return a list of all detected bugs in the database.
    """
    bugs = db.query(Bug).all()
    return bugs

@router.get("/bugs/{bug_id}", response_model=BugResponse)
def get_bug_by_id(bug_id: str, db: Session = Depends(get_db)):
    """
    GET /api/bugs/{bug_id}
    Return detailed information for a specific bug by ID.
    """
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail=f"Bug record {bug_id} not found.")
    return bug
