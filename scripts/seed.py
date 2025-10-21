"""
Seed script for Resort Tracker — inserts demo tasks.
Run: python scripts/seed.py
"""

from app.db import engine, get_session
from app.models import Task
from sqlmodel import SQLModel

demo_tasks = [
    Task(
        title="Check AC compressor in Room 302",
        category="engineering",
        priority="high",
        assigned_to="Azlan",
    ),
    Task(
        title="Replace light bulb at lobby entrance",
        category="housekeeping",
        priority="medium",
        assigned_to="Syahmi",
    ),
    Task(
        title="Clean main pool filter",
        category="engineering",
        priority="medium",
        assigned_to="Ridzuan",
    ),
    Task(
        title="Refill minibar in Chalet 12",
        category="front_office",
        priority="low",
        assigned_to="Aiman",
    ),
]


def seed():
    SQLModel.metadata.create_all(engine)
    with get_session() as session:
        for task in demo_tasks:
            session.add(task)
        session.commit()
    print(f"Inserted {len(demo_tasks)} demo tasks ✅")


if __name__ == "__main__":
    seed()
