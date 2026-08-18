# Ownership: Pavan (API + Static Analysis + Database)
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from datetime import datetime
from models import Base

class Fix(Base):
    __tablename__ = "fixes"

    id = Column(String, primary_key=True, index=True)
    bug_id = Column(String, ForeignKey("bugs.id"))
    fixed_code = Column(Text)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
