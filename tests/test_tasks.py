import os
import tempfile
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session
from app.main import app
from app import db, models

# Isolate a temp DB for tests
def setup_module(module):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    os.environ["TEST_DB"] = tmp.name  # not used directly, but kept for clarity
    db.engine = create_engine(f"sqlite:///{tmp.name}")
    SQLModel.metadata.create_all(db.engine)

client = TestClient(app)

def test_create_task_minimal():
    payload = {"title": "AC not cooling in Room 103"}
    r = client.post("/tasks", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == payload["title"]
    assert body["status"] == "open"

def test_update_status_flow():
    r = client.post("/tasks", json={"title": "Check pool pump"})
    task_id = r.json()["id"]
    r2 = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "in_progress"

def test_delete_task():
    r = client.post("/tasks", json={"title": "Replace light bulb"})
    task_id = r.json()["id"]
    r2 = client.delete(f"/tasks/{task_id}")
    assert r2.status_code == 204
    r3 = client.get(f"/tasks/{task_id}")
    assert r3.status_code == 404
