from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import jwt, JWTError
from app.db import engine
from app.models import User
from app.schemas import UserCreate, UserRead, Token
from app.utils.security import hash_password, verify_password, create_access_token
from app.settings import settings


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/signup", response_model=UserRead, status_code=201)
def signup(payload: UserCreate):
    # 1️⃣ Manager signup requires correct admin code
    if payload.role == "manager" and payload.admin_code != settings.ADMIN_SIGNUP_CODE:
        raise HTTPException(status_code=403, detail="Invalid admin code")

    with Session(engine) as s:
        # 2️⃣ Check if email exists
        existing_user = s.exec(select(User).where(User.email == payload.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # 3️⃣ Hash the password before saving
        hashed_pw = hash_password(payload.password)

        # 4️⃣ Create user directly (not from_orm)
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hashed_pw,
            role=payload.role,
        )

        s.add(user)
        s.commit()
        s.refresh(user)
        return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.email == form_data.username)).first()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

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
        raise HTTPException(status_code=401, detail="Invalid token")

    with Session(engine) as s:
        user = s.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Inactive or invalid user")
        return user


def require_manager(current: User = Depends(get_current_user)) -> User:
    if current.role != "manager":
        raise HTTPException(status_code=403, detail="Managers only")
    return current
