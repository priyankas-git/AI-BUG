# Ownership: Pavan (API + Static Analysis + Database)
from pydantic import BaseModel
from typing import Optional

class ValidationRequest(BaseModel):
    bug_id: str
    fixed_code: str

class ValidationResponse(BaseModel):
    bug_id: str
    status: str # "RESOLVED" or "FAILED"
    syntax_check: bool
    static_analysis: bool
    test_run: bool
    passed: bool
    message: Optional[str] = None

    class Config:
        from_attributes = True
