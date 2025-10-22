# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from app.main import app
from app.db import engine
from app.settings import settings

print("\n=== 🧪 Pytest setup ===")

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Ensure the app runs in test mode and uses .env.test.
    """
    os.environ["ENV"] = "test"
    # If you want to verify it's using the test DB, uncomment below:
    # from app.settings import settings
    # print("🧪 Using DB:", settings.DATABASE_URL)
    yield

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Initialize the test database schema once before all tests.
    Drops & recreates all tables to ensure a clean test environment.
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    # optional cleanup after all tests
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def client():
    """
    Provides a fresh TestClient for each test.
    """
    with TestClient(app) as c:
        yield c
