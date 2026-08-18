# Ownership: Pavan (API + Static Analysis + Database)
from pydantic import BaseModel

class FixRequest(BaseModel):
    bug_id: str

class FixResponse(BaseModel):
    bug_id: str
    fixed_code: str
    explanation: str

    class Config:
        from_attributes = True
