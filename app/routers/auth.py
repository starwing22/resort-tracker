from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from app.db import get_session
from app.models import User
from app.schemas import UserCreate, UserRead, Token, Login
from app.utils.security import hash_password, verify_password, create_access_token
from app.settings import settings
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/signup", response_model=UserRead, status_code=201)
def signup(payload: UserCreate):

# managers need a code
    if payload.role == "manager" and payload.admin_code != settings.ADMIN_SIGNUP_CODE:
        raise HTTPException(403, "Invalid admin code")

    with get_session() as s:
        exists = s.exec(select(User).where(User.email == payload.email)).first()
        if exists:
            raise HTTPException(400, "Email already registered")
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            role=payload.role,
            hashed_password=hash_password(payload.password),
        )
        s.add(user)
        s.commit()
        s.refresh(user)
        return UserRead(**user.model_dump())

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_session() as s:
        user = s.exec(select(User).where(User.email == form_data.username)).first()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(400, "Incorrect email or password")
        token = create_access_token(
            subject=str(user.id),
            secret=settings.SECRET_KEY,
            expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        return Token(access_token=token)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub", "0"))
    except JWTError:
        raise HTTPException(401, "Invalid token")

    with get_session() as s:
        user = s.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(401, "Inactive or invalid user")
        return user

def require_manager(current=Depends(get_current_user)) -> User:
    if current.role != "manager":
        raise HTTPException(403, "Managers only")
    return current
