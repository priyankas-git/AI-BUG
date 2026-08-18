# Ownership: Pavan (API + Static Analysis + Database)
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.bug import Bug
from models.test_result import TestResult
from schemas.validation import ValidationRequest, ValidationResponse
from services.validation_service import ValidationService

router = APIRouter()

validation_service = ValidationService()

@router.post("/validate", response_model=ValidationResponse)
def validate_fix(payload: ValidationRequest, db: Session = Depends(get_db)):
    """
    POST /api/validate
    Executes compilation checks, static checker rules, and dynamic assertions on the proposed fix.
    """
    # 1. Fetch bug record
    bug = db.query(Bug).filter(Bug.id == payload.bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail=f"Bug record {payload.bug_id} not found.")

    # 2. Retrieve original source code reference
    original_code = ""
    if os.path.exists(bug.file):
        try:
            with open(bug.file, "r", encoding="utf-8") as f:
                original_code = f.read()
        except Exception:
            pass

    # 3. Call Validation pipeline
    language = "python" if bug.file.endswith(".py") else "javascript"
    
    try:
        val_res = validation_service.validate(
            language=language,
            original_code=original_code,
            fixed_code=payload.fixed_code,
            test_case=bug.test_case or ""
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation service error: {str(e)}")

    # 4. Update Database
    status = "RESOLVED" if val_res["passed"] else "OPEN"
    bug.status = status
    bug.fixed_code = payload.fixed_code

    # Create dynamic test log record
    test_log = TestResult(
        id=f"TR-{uuid.uuid4().hex[:6].upper()}",
        bug_id=bug.id,
        syntax_check=val_res["syntax_check"],
        static_analysis=val_res["static_analysis"],
        test_run=val_res["test_run"],
        passed=val_res["passed"],
        message=val_res["message"]
    )
    db.add(test_log)
    db.commit()
    
    db.refresh(bug)

    return {
        "bug_id": bug.id,
        "status": status,
        "syntax_check": val_res["syntax_check"],
        "static_analysis": val_res["static_analysis"],
        "test_run": val_res["test_run"],
        "passed": val_res["passed"],
        "message": val_res["message"]
    }
