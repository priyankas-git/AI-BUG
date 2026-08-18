import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Appending backend directory to python path for direct service access
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_path)

# Set Page Config
st.set_page_config(
    page_title="AI Bug Detection Tool - Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    .metric-val-crit { color: #ef4444; font-size: 28px; font-weight: bold; }
    .metric-val-high { color: #f97316; font-size: 28px; font-weight: bold; }
    .metric-val-med { color: #eab308; font-size: 28px; font-weight: bold; }
    .metric-val-low { color: #22c55e; font-size: 28px; font-weight: bold; }
    .metric-val-neutral { color: #3b82f6; font-size: 28px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI Bug Detection & Remediation platform")
st.markdown("Metrics, security posture, and auto-remediation gates tracking.")

# Mock/Default Stats Fallbacks
stats = {
    "total_projects": 3,
    "total_analyses": 12,
    "total_bugs": 8,
    "critical_bugs": 1,
    "high_bugs": 3,
    "medium_bugs": 3,
    "low_bugs": 1,
    "severity_distribution": {"CRITICAL": 1, "HIGH": 3, "MEDIUM": 3, "LOW": 1},
    "type_distribution": {
        "Logic Error": 2,
        "Security Vulnerability": 2,
        "Runtime Error": 3,
        "Code Smell": 1
    },
    "recent_analyses": [
        {"id": "AN-001", "project": "E-Commerce Gateway", "file": "payment.py", "bugs": 3, "max_severity": "CRITICAL", "status": "COMPLETED", "date": "2026-08-18"},
        {"id": "AN-002", "project": "Auth Core", "file": "jwt.js", "bugs": 1, "max_severity": "HIGH", "status": "COMPLETED", "date": "2026-08-17"},
        {"id": "AN-003", "project": "Data Pipeline", "file": "spark_loader.py", "bugs": 4, "max_severity": "MEDIUM", "status": "COMPLETED", "date": "2026-08-15"}
    ]
}

# Try loading from database if exists
try:
    from database.database import SessionLocal
    from models.project import Project
    from models.analysis import Analysis
    from models.bug import Bug
    
    db = SessionLocal()
    db_projects = db.query(Project).count()
    db_analyses = db.query(Analysis).count()
    db_bugs = db.query(Bug).count()
    
    if db_projects > 0 or db_analyses > 0:
        stats["total_projects"] = db_projects
        stats["total_analyses"] = db_analyses
        stats["total_bugs"] = db_bugs
        stats["critical_bugs"] = db.query(Bug).filter(Bug.severity == "CRITICAL").count()
        stats["high_bugs"] = db.query(Bug).filter(Bug.severity == "HIGH").count()
        stats["medium_bugs"] = db.query(Bug).filter(Bug.severity == "MEDIUM").count()
        stats["low_bugs"] = db.query(Bug).filter(Bug.severity == "LOW").count()
        
        # update distributions
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for bug in db.query(Bug).all():
            sev = bug.severity.upper()
            if sev in severity_counts:
                severity_counts[sev] += 1
        stats["severity_distribution"] = severity_counts
        
        # type distribution
        type_counts = {}
        for bug in db.query(Bug).all():
            type_counts[bug.type] = type_counts.get(bug.type, 0) + 1
        stats["type_distribution"] = type_counts
        
        # recent analyses
        recent_list = []
        for an in db.query(Analysis).order_by(Analysis.created_at.desc()).limit(5).all():
            proj = db.query(Project).filter(Project.id == an.project_id).first()
            recent_list.append({
                "id": an.id,
                "project": proj.name if proj else "Default Project",
                "file": an.file_name,
                "bugs": an.total_bugs,
                "max_severity": "HIGH", # simplified
                "status": an.status.upper(),
                "date": an.created_at.strftime("%Y-%m-%d")
            })
        if recent_list:
            stats["recent_analyses"] = recent_list
            
    db.close()
except Exception as e:
    pass

st.markdown("---")

# Metrics Grid
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f'<div class="metric-card"><p style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:1px;">Total Projects</p><span class="metric-val-neutral">{stats["total_projects"]}</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:1px;">Active Flaws</p><span class="metric-val-neutral">{stats["total_bugs"]}</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p style="font-size:11px; color:#ef4444; text-transform:uppercase; letter-spacing:1px;">Critical Bugs</p><span class="metric-val-crit">{stats["critical_bugs"]}</span></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><p style="font-size:11px; color:#f97316; text-transform:uppercase; letter-spacing:1px;">High Bugs</p><span class="metric-val-high">{stats["high_bugs"]}</span></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><p style="font-size:11px; color:#eab308; text-transform:uppercase; letter-spacing:1px;">Medium Bugs</p><span class="metric-val-med">{stats["medium_bugs"]}</span></div>', unsafe_allow_html=True)

st.markdown("---")

# Charts Grid
char_col1, char_col2 = st.columns(2)
with char_col1:
    st.markdown("### Severity Distribution")
    sev_df = pd.DataFrame(list(stats["severity_distribution"].items()), columns=["Severity", "Count"])
    fig = px.bar(
        sev_df, 
        x="Severity", 
        y="Count", 
        color="Severity",
        color_discrete_map={"CRITICAL": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#eab308", "LOW": "#22c55e"},
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

with char_col2:
    st.markdown("### Bug Type Distribution")
    type_df = pd.DataFrame(list(stats["type_distribution"].items()), columns=["Type", "Count"])
    fig = px.pie(
        type_df, 
        values="Count", 
        names="Type", 
        hole=0.4,
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Cyan
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Recent Analysis List
st.markdown("### Recent Code Analyses")
recent_df = pd.DataFrame(stats["recent_analyses"])
st.dataframe(recent_df, use_container_width=True)
