# app/db.py
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine, Session
from app.settings import settings
from contextlib import contextmanager
from typing import Iterator


RAW_URL = settings.DATABASE_URL

def make_engine(url: str):
    # In-memory / SQLite → no pool_size/max_overflow, special pool for tests
    if url.startswith("sqlite://"):
        # For in-memory DBs, share one connection across threads
        if url in ("sqlite://", "sqlite:///:memory:"):
            return create_engine(
                "sqlite://",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False,
            )
        # File-based SQLite
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            echo=False,
        )

    # Postgres (Render, local dev, etc.)
    # Normalize driver if needed (postgres:// → postgresql+psycopg://)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    # Safe small pool for free-tier services
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=0,
        echo=False,
    )

engine = make_engine(RAW_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
    
@contextmanager
def get_session() -> Iterator[Session]:
    """Use with: `with get_session() as s:`"""
    with Session(engine) as session:
        yield session
