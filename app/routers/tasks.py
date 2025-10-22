from __future__ import annotations
from typing import List, Optional
from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import or_  # use SQLAlchemy's or_
from sqlmodel import select

from app.db import get_session
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, TaskRead
from app.routers.auth import get_current_user, require_manager

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskRead])
def list_tasks(
    status: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None, description="search title/description"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    current: User = Depends(get_current_user),
):
    with get_session() as s:
        stmt = select(Task)

        # Staff see only their assigned tasks
        if current.role == "staff":
            stmt = stmt.where(Task.assigned_user_id == current.id)

        if status:
            stmt = stmt.where(Task.status == status)
        if category:
            stmt = stmt.where(Task.category == category)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(or_(Task.title.ilike(like), Task.description.ilike(like)))

        stmt = stmt.order_by(Task.created_at.desc()).limit(limit).offset(offset)
        return s.exec(stmt).all()


@router.post("", response_model=TaskRead, status_code=201, dependencies=[Depends(require_manager)])
def create_task(payload: TaskCreate, current: User = Depends(get_current_user)):
    with get_session() as s:
        task = Task(**payload.model_dump(), created_by_id=current.id)
        s.add(task)
        s.commit()
        s.refresh(task)
        return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, current: User = Depends(get_current_user)):
    with get_session() as s:
        task = s.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        if current.role == "staff" and task.assigned_user_id != current.id:
            raise HTTPException(403, "Not your task")

        return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, current: User = Depends(get_current_user)):
    with get_session() as s:
        task = s.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        data = payload.model_dump(exclude_unset=True)

        if current.role == "manager":
            # manager: full access
            pass
        else:
            # staff: can only update own tasks + only some fields
            if task.assigned_user_id != current.id:
                raise HTTPException(403, "Not your task")
            allowed = {"status", "description"}
            data = {k: v for k, v in data.items() if k in allowed}

        for k, v in data.items():
            setattr(task, k, v)

        task.updated_at = datetime.now(UTC)
        s.add(task)
        s.commit()
        s.refresh(task)
        return task


@router.delete("/{task_id}", status_code=204, dependencies=[Depends(require_manager)])
def delete_task(task_id: int):
    with get_session() as s:
        task = s.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        s.delete(task)
        s.commit()
        return
