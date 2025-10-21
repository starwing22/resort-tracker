from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel

Status = Literal["open", "in_progress", "completed"]
Priority = Literal["low", "medium", "high"]
Category = Literal["engineering", "housekeeping", "front_office", "other"]


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status = "open"
    assigned_to: Optional[str] = None
    priority: Priority = "medium"
    category: Category = "engineering"
    due_date: Optional[date] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    assigned_to: Optional[str] = None
    priority: Optional[Priority] = None
    category: Optional[Category] = None
    due_date: Optional[date] = None


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
