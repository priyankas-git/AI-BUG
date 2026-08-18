# Ownership: Pavan (API + Static Analysis + Database)
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from models import Base

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(String, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    type = Column(String, index=True)
    severity = Column(String, index=True)
    confidence = Column(Float, default=1.0)
    file = Column(String)
    line = Column(Integer)
    description = Column(Text)
    explanation = Column(Text)
    impact = Column(Text)
    suggestion = Column(Text)
    fixed_code = Column(Text)
    test_case = Column(Text)
    status = Column(String, default="OPEN") # OPEN, RESOLVED
