# Ownership: Pavan (API + Static Analysis + Database)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.project import Project
from models.analysis import Analysis
from models.bug import Bug
from schemas.analysis import DashboardStatsResponse

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    GET /api/dashboard
    Runs queries across database tables to aggregate counts and distributions.
    """
    # 1. Base counts
    total_projects = db.query(Project).count()
    total_analyses = db.query(Analysis).count()
    total_bugs = db.query(Bug).count()
    
    # 2. Severity Counts
    critical_bugs = db.query(Bug).filter(Bug.severity == "CRITICAL").count()
    high_bugs = db.query(Bug).filter(Bug.severity == "HIGH").count()
    medium_bugs = db.query(Bug).filter(Bug.severity == "MEDIUM").count()
    low_bugs = db.query(Bug).filter(Bug.severity == "LOW").count()
    
    # 3. Distributions
    bug_severity_distribution = {
        "CRITICAL": critical_bugs,
        "HIGH": high_bugs,
        "MEDIUM": medium_bugs,
        "LOW": low_bugs
    }
    
    bug_type_distribution = {}
    for bug in db.query(Bug).all():
        bug_type_distribution[bug.type] = bug_type_distribution.get(bug.type, 0) + 1
        
    # 4. Recent analyses list
    recent_runs = []
    analyses = db.query(Analysis).order_by(Analysis.created_at.desc()).limit(5).all()
    for an in analyses:
        proj = db.query(Project).filter(Project.id == an.project_id).first()
        recent_runs.append({
            "id": an.id,
            "project": proj.name if proj else "Default Project",
            "file": an.file_name,
            "bug_count": an.total_bugs,
            "severity": "CRITICAL" if an.critical_bugs > 0 else ("HIGH" if an.high_bugs > 0 else "MEDIUM"),
            "status": an.status,
            "date": an.created_at.strftime("%Y-%m-%d")
        })

    return {
        "total_projects": total_projects,
        "total_analyses": total_analyses,
        "total_bugs": total_bugs,
        "critical_bugs": critical_bugs,
        "high_bugs": high_bugs,
        "medium_bugs": medium_bugs,
        "low_bugs": low_bugs,
        "bug_severity_distribution": bug_severity_distribution,
        "bug_type_distribution": bug_type_distribution,
        "recent_analyses": recent_runs
    }
