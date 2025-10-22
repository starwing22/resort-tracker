from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select

from app.db import get_session
from app.models import User
from app.schemas import UserRead
from app.routers.auth import require_manager

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserRead], dependencies=[Depends(require_manager)])
def list_users():
    with get_session() as s:
        return s.exec(select(User).order_by(User.full_name)).all()
