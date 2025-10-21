# NEW imports
from enum import Enum
from datetime import datetime, date, UTC
from sqlmodel import SQLModel, Field
from typing import Optional

# ----- Enums -----
class RoleEnum(str, Enum):
    manager = "manager"
    staff = "staff"

class StatusEnum(str, Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class CategoryEnum(str, Enum):
    engineering = "engineering"
    housekeeping = "housekeeping"
    front_office = "front_office"
    other = "other"

# ----- Models -----
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: StatusEnum = Field(default=StatusEnum.open)
    assigned_to: Optional[str] = None
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    category: CategoryEnum = Field(default=CategoryEnum.engineering)
    due_date: Optional[date] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    role: RoleEnum = Field(default=RoleEnum.staff)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
