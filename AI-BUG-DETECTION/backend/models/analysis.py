# Ownership: Pavan (API + Static Analysis + Database)
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from datetime import datetime
from models import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    file_name = Column(String, index=True)
    status = Column(String, default="completed")
    total_bugs = Column(Integer, default=0)
    critical_bugs = Column(Integer, default=0)
    high_bugs = Column(Integer, default=0)
    medium_bugs = Column(Integer, default=0)
    low_bugs = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
