from datetime import datetime, timedelta, UTC
from jose import jwt
from passlib.hash import argon2

def hash_password(password: str) -> str:
    return argon2.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return argon2.verify(plain, hashed)

def create_access_token(subject: str, secret: str, expires_minutes: int) -> str:
    exp = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    return jwt.encode({"sub": subject, "exp": exp}, secret, algorithm="HS256")
