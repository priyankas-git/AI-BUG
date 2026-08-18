# Ownership: Pavan (API + Static Analysis + Database)
import sys
import os

# Add parent directory to path so imports work when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import engine
from models import Base
# Import models to ensure they are registered with Base metadata
from models.project import Project
from models.analysis import Analysis
from models.bug import Bug
from models.fix import Fix
from models.test_result import TestResult

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
