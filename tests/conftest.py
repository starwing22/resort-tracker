import os, tempfile, pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine
from app.main import app
from app import db

@pytest.fixture(scope="function")
def client():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db.engine = create_engine(f"sqlite:///{tmp.name}", connect_args={"check_same_thread": False})
    with TestClient(app) as c:  # runs lifespan -> init_db()
        yield c
    os.unlink(tmp.name)
