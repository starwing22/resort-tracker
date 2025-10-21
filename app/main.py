from fastapi import FastAPI
from app.db import init_db
from app.routers import tasks

app = FastAPI(title="Resort Task Tracker", version="0.1.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(tasks.router)

@app.get("/health")
def health():
    return {"ok": True}
