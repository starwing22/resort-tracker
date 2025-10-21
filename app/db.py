# app/db.py
import os
from sqlalchemy.engine.url import make_url
from sqlmodel import SQLModel, create_engine, Session

def _normalize_db_url(raw: str) -> str:
    if raw.startswith("postgres://"):
        raw = raw.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw.startswith("postgresql://"):
        raw = raw.replace("postgresql://", "postgresql+psycopg://", 1)
    # Ensure sslmode=require for external connections (safe if duplicated)
    if "sslmode=" not in raw:
        sep = "&" if "?" in raw else "?"
        raw = f"{raw}{sep}sslmode=require"
    # Validate URL
    make_url(raw)
    return raw

RAW_URL = os.getenv("DATABASE_URL", "sqlite:///./resort_tasks.db")
SQLALCHEMY_URL = _normalize_db_url(RAW_URL) if RAW_URL.startswith("postg") else RAW_URL

engine = create_engine(
    SQLALCHEMY_URL,
    pool_pre_ping=True,
    pool_size=5,           # keep small on free tier
    max_overflow=0,
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
