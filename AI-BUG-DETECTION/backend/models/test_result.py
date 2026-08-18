# Ownership: Pavan (API + Static Analysis + Database)
from sqlalchemy import Column, String, Boolean, ForeignKey, Text, DateTime
from datetime import datetime
from models import Base

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(String, primary_key=True, index=True)
    bug_id = Column(String, ForeignKey("bugs.id"))
    syntax_check = Column(Boolean, default=False)
    static_analysis = Column(Boolean, default=False)
    test_run = Column(Boolean, default=False)
    passed = Column(Boolean, default=False)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
