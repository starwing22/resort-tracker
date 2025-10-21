from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.routers import tasks


# define lifespan BEFORE creating FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield  # startup complete, app is ready


# now you can safely use lifespan below
app = FastAPI(title="Resort Tracker", version="0.1.0", lifespan=lifespan)

app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"ok": True}
