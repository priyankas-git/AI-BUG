# Ownership: Pavan (API + Static Analysis + Database)
from pydantic import BaseModel, Field
from typing import Optional

class BugResponse(BaseModel):
    id: str
    type: str
    severity: str
    confidence: float = Field(..., serialization_alias="confidence_score", validation_alias="confidence")
    file: str
    line: int
    description: str
    explanation: str
    impact: str
    suggestion: str
    fixed_code: Optional[str] = None
    test_case: Optional[str] = None
    status: str = "OPEN"

    class Config:
        populate_by_name = True
        from_attributes = True
