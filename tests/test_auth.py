# tests/test_auth.py
from app.settings import settings

def test_signup_and_login_manager(client):
    # signup manager
    r = client.post("/auth/signup", json={
        "email": "manager@example.com",
        "full_name": "Manager One",
        "password": "secret123",
        "role": "manager",
        "admin_code": settings.ADMIN_SIGNUP_CODE,  # use app value
    })
    assert r.status_code in (200, 201), f"SIGNUP failed: {r.status_code} {r.text}"

    # login
    r2 = client.post("/auth/login", data={
        "username": "manager@example.com",
        "password": "secret123",
    })
    assert r2.status_code == 200, f"LOGIN failed: {r2.status_code} {r2.text}"
    token = r2.json()["access_token"]

    # create a task as manager (sanity)
    headers = {"Authorization": f"Bearer {token}"}
    r3 = client.post("/tasks", json={"title": "Test Task"}, headers=headers)
    assert r3.status_code == 201, f"TASK create failed: {r3.status_code} {r3.text}"
