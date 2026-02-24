from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.jwt.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.app.secret_key.get_secret_value(),
        algorithm=settings.jwt.algorithm
    )
    return encoded_jwt