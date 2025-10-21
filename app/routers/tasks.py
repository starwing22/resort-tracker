from typing import List
from datetime import UTC, datetime
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskRead])
def list_tasks(
    status: str | None = Query(default=None),
    assigned_to: str | None = Query(default=None),
    category: str | None = Query(default=None),
):
    with get_session() as s:
        stmt = select(Task)
        if status:
            stmt = stmt.where(Task.status == status)
        if assigned_to:
            stmt = stmt.where(Task.assigned_to == assigned_to)
        if category:
            stmt = stmt.where(Task.category == category)
        return s.exec(stmt).all()


@router.post("", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate):
    with get_session() as s:
        task = Task(**payload.model_dump())
        s.add(task)
        s.commit()
        s.refresh(task)
        return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    with get_session() as s:
        task = s.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate):
    with get_session() as s:
        task = s.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(task, k, v)
        task.updated_at = datetime.now(UTC)
        s.add(task)
        s.commit()
        s.refresh(task)
        return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_session() as s:
        task = s.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        s.delete(task)
        s.commit()
        return
