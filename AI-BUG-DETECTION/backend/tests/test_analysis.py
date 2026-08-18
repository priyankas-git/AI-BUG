# Ownership: Pavan (API + Static Analysis + Database)
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "AI Bug Detection Backend"
    }
