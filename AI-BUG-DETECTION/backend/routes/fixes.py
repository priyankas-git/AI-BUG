# Ownership: Pavan (API + Static Analysis + Database)
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.bug import Bug
from schemas.fix import FixRequest, FixResponse
from services.fix_generator import FixGenerator

router = APIRouter()

fix_generator = FixGenerator()

@router.post("/fix", response_model=FixResponse)
def generate_fix(payload: FixRequest, db: Session = Depends(get_db)):
    """
    POST /api/fix
    Triggers the LangChain LLM engine to generate a fixed version of code for the given bug.
    """
    # 1. Fetch bug record
    bug = db.query(Bug).filter(Bug.id == payload.bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail=f"Bug record {payload.bug_id} not found.")

    # 2. Retrieve original source code
    original_code = ""
    # Try loading from local file if exists
    if os.path.exists(bug.file):
        try:
            with open(bug.file, "r", encoding="utf-8") as f:
                original_code = f.read()
        except Exception:
            original_code = bug.fixed_code or ""
    else:
        original_code = bug.fixed_code or ""

    # 3. Call Fix Generator
    language = "python" if bug.file.endswith(".py") else "javascript"
    
    try:
        result = fix_generator.generate_fix(
            language=language,
            original_code=original_code,
            bug_details={
                "line": bug.line,
                "type": bug.type,
                "description": bug.description
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed generating fix: {str(e)}")

    # 4. Save proposal to database
    bug.fixed_code = result["fixed_code"]
    db.commit()
    db.refresh(bug)

    return {
        "bug_id": bug.id,
        "fixed_code": result["fixed_code"],
        "explanation": result["explanation"]
    }
