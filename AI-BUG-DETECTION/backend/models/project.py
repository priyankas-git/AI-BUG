# Ownership: Pavan (API + Static Analysis + Database)
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from models import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
