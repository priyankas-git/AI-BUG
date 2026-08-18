# Ownership: Pavan (API + Static Analysis + Database)
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.project import Project
from models.analysis import Analysis
from models.bug import Bug
from schemas.analysis import AnalysisRequest, AnalysisResponse
from services.static_analyzer import StaticAnalyzer
from services.ai_analyzer import AIAnalyzer
from services.result_fusion import ResultFusion

router = APIRouter()

static_analyzer = StaticAnalyzer()
ai_analyzer = AIAnalyzer()
result_fusion = ResultFusion()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_code(payload: AnalysisRequest, db: Session = Depends(get_db)):
    """
    POST /api/analyze
    Analyzes submitted code, persists findings, and returns the analysis summary report.
    """
    # 1. Establish project context
    project_id = payload.project_id
    if not project_id:
        # Check or create default project
        default_proj = db.query(Project).filter(Project.name == "Default Project").first()
        if not default_proj:
            default_proj = Project(id="PRJ-001", name="Default Project")
            db.add(default_proj)
            db.commit()
            db.refresh(default_proj)
        project_id = default_proj.id
    else:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Specified Project ID not found.")

    # 2. Execute analysis engines
    try:
        static_flaws = static_analyzer.analyze(payload.language, payload.code, payload.file_name)
        ai_flaws = ai_analyzer.analyze_code(payload.language, payload.code, payload.file_name)
        fused_flaws = result_fusion.fuse(static_res=static_flaws, ai_results=ai_flaws)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline crash: {str(e)}")

    # 3. Create Analysis database record
    analysis_id = f"AN-{uuid.uuid4().hex[:6].upper()}"
    
    # Calculate summary levels
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in fused_flaws:
        sev = f.get("severity", "MEDIUM").upper()
        if sev in counts:
            counts[sev] += 1

    analysis = Analysis(
        id=analysis_id,
        project_id=project_id,
        file_name=payload.file_name,
        status="completed",
        total_bugs=len(fused_flaws),
        critical_bugs=counts["CRITICAL"],
        high_bugs=counts["HIGH"],
        medium_bugs=counts["MEDIUM"],
        low_bugs=counts["LOW"]
    )
    db.add(analysis)

    # 4. Save Bug objects
    bugs_response_list = []
    for idx, flaw in enumerate(fused_flaws):
        bug_id = f"BUG-{uuid.uuid4().hex[:6].upper()}"
        
        bug_db = Bug(
            id=bug_id,
            analysis_id=analysis_id,
            type=flaw.get("type", "Logic Error"),
            severity=flaw.get("severity", "MEDIUM").upper(),
            confidence=float(flaw.get("confidence", 0.9)),
            file=flaw.get("file", payload.file_name),
            line=int(flaw.get("line", 1)),
            description=flaw.get("description", ""),
            explanation=flaw.get("explanation", ""),
            impact=flaw.get("impact", ""),
            suggestion=flaw.get("suggestion", ""),
            fixed_code=flaw.get("fixed_code"),
            test_case=flaw.get("test_case"),
            status="OPEN"
        )
        db.add(bug_db)
        
        # Prepare response schema values
        bugs_response_list.append(bug_db)

    db.commit()
    
    # Re-fetch models to avoid session detach issues
    db.refresh(analysis)
    for b in bugs_response_list:
        db.refresh(b)

    return {
        "analysis_id": analysis.id,
        "status": analysis.status,
        "summary": {
            "total_bugs": analysis.total_bugs,
            "critical": analysis.critical_bugs,
            "high": analysis.high_bugs,
            "medium": analysis.medium_bugs,
            "low": analysis.low_bugs
        },
        "bugs": bugs_response_list
    }
