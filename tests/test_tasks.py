# tests/test_tasks.py
from app.settings import settings

def _manager_headers(client):
    """Ensure a manager exists, then login and return Bearer headers."""
    # Try to sign up (idempotent: ignore 'already registered' errors)
    client.post("/auth/signup", json={
        "email": "manager@example.com",
        "full_name": "Manager One",
        "password": "secret123",
        "role": "manager",
        "admin_code": settings.ADMIN_SIGNUP_CODE,
    })
    # Login
    r = client.post("/auth/login", data={
        "username": "manager@example.com",
        "password": "secret123",
    })
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_task_minimal(client):
    headers = _manager_headers(client)
    payload = {"title": "AC not cooling in Room 103"}
    r = client.post("/tasks", json=payload, headers=headers)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["id"] > 0
    assert body["title"] == payload["title"]
    assert body["status"] == "open"


def test_update_status_flow(client):
    headers = _manager_headers(client)

    # create
    r = client.post("/tasks", json={"title": "Check pool pump"}, headers=headers)
    assert r.status_code == 201, r.text
    task_id = r.json()["id"]

    # update status
    r2 = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"}, headers=headers)
    assert r2.status_code == 200, r2.text
    assert r2.json()["status"] == "in_progress"

    # fetch & confirm
    r3 = client.get(f"/tasks/{task_id}", headers=headers)
    assert r3.status_code == 200, r3.text
    assert r3.json()["status"] == "in_progress"


def test_delete_task(client):
    headers = _manager_headers(client)

    # create
    r = client.post("/tasks", json={"title": "Replace light bulb"}, headers=headers)
    assert r.status_code == 201, r.text
    task_id = r.json()["id"]

    # delete
    r2 = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r2.status_code == 204, r2.text

    # confirm gone
    r3 = client.get(f"/tasks/{task_id}", headers=headers)
    assert r3.status_code == 404, r3.text
