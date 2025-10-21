from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager

SQLITE_URL = "sqlite:///./resort_tasks.db"
engine = create_engine(SQLITE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
