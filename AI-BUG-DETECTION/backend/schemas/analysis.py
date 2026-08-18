# Ownership: Pavan (API + Static Analysis + Database)
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
from schemas.bug import BugResponse

class AnalysisRequest(BaseModel):
    language: str
    code: str
    file_name: str
    project_id: Optional[str] = None

class AnalysisSummary(BaseModel):
    total_bugs: int
    critical: int
    high: int
    medium: int
    low: int

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    summary: AnalysisSummary
    bugs: List[BugResponse]

    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardStatsResponse(BaseModel):
    total_projects: int
    total_analyses: int
    total_bugs: int
    critical_bugs: int
    high_bugs: int
    medium_bugs: int
    low_bugs: int
    bug_severity_distribution: Dict[str, int]
    bug_type_distribution: Dict[str, int]
    recent_analyses: List[Dict[str, Any]] = []
