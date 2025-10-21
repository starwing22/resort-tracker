from typing import Optional
from datetime import datetime, date, UTC
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="open")  # open | in_progress | completed
    assigned_to: Optional[str] = None
    priority: str = Field(default="medium")  # low | medium | high
    category: str = Field(default="engineering")  # engineering | housekeeping | front_office | other
    due_date: Optional[date] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
