from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import init_db
from app.settings import settings
from app.routers import tasks,auth


# define lifespan BEFORE creating FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield  # startup complete, app is ready


app = FastAPI(title="Resort Task Tracker", version="0.2.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/health")
def health():
    return {"ok": True}
