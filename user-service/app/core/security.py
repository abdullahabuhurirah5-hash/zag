from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings

password_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_ALGO = "HS256"


def hash_password(plain: str) -> str:
    return password_manager.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_manager.verify(plain, hashed)


def generate_token(user_id: int, minutes: Optional[int] = None) -> str:
    expiry_minutes = minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=expiry_minutes),
    }
    return jwt.encode(
        payload,
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=JWT_ALGO,
    )
