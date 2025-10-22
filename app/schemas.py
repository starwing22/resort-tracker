from __future__ import annotations
from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel, EmailStr


# ---------- Task ----------

Status = Literal["open", "in_progress", "completed"]
Priority = Literal["low", "medium", "high"]
Category = Literal["engineering", "housekeeping", "front_office", "other"]

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status = "open"
    priority: Priority = "medium"
    category: Category = "engineering"
    due_date: Optional[date] = None
    assigned_user_id: Optional[int] = None  # FK to User.id

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    category: Optional[Category] = None
    due_date: Optional[date] = None
    assigned_user_id: Optional[int] = None

class TaskRead(TaskBase):
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# ---------- User (read-only here; create handled in auth schemas) ----------

Role = Literal["manager", "staff"]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: Role
    is_active: bool

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    role: str = "staff"          # simple string; enforce choices at the router/service layer
    admin_code: Optional[str] = None  # required if role == "manager"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
