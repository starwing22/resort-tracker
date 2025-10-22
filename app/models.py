from typing import Optional, List
from datetime import datetime, date, UTC
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    role: str = Field(default="staff")
    hashed_password: str
    is_active: bool = True

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)

    # IMPORTANT: use List["Task"] (capital L), not list["Task"]
    created_tasks: List["Task"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "foreign_keys": "[Task.created_by_id]",
        },
    )
    assigned_tasks: List["Task"] = Relationship(
        back_populates="assigned_user",
        sa_relationship_kwargs={
            "foreign_keys": "[Task.assigned_user_id]",
        },
    )


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="open")           # open | in_progress | completed
    priority: str = Field(default="medium")       # low | medium | high
    category: str = Field(default="engineering")  # engineering | housekeeping | front_office | other
    due_date: Optional[date] = None

    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    assigned_user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)

    # Quote forward refs on the single ends too
    created_by: Optional["User"] = Relationship(
        back_populates="created_tasks",
        sa_relationship_kwargs={
            "primaryjoin": "Task.created_by_id==User.id",
            "foreign_keys": "[Task.created_by_id]",
            "lazy": "joined",
        },
    )
    assigned_user: Optional["User"] = Relationship(
        back_populates="assigned_tasks",
        sa_relationship_kwargs={
            "primaryjoin": "Task.assigned_user_id==User.id",
            "foreign_keys": "[Task.assigned_user_id]",
            "lazy": "joined",
        },
    )
