from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# import the enums defined in models
from app.models import (
    StatusEnum, PriorityEnum, CategoryEnum, RoleEnum
)

# ---- Task schemas ----
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.open
    assigned_to: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.medium
    category: CategoryEnum = CategoryEnum.engineering
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    assigned_to: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[CategoryEnum] = None
    due_date: Optional[date] = None

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ---- User/Auth schemas ----
class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    role: RoleEnum = RoleEnum.staff
    admin_code: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: RoleEnum
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    email: EmailStr
    password: str
