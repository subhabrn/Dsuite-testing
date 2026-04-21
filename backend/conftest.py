import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import after path adjustment
from main import app
from core.db.database import get_db, Base
from core.db.database import engine, SessionLocal

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db_session():
    """Creates a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def pytest_configure(config):
    """Setup pytest configuration."""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
