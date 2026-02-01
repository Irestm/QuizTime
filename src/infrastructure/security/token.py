from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.app.secret_key.get_secret_value(), algorithm=settings.jwt.algorithm)
    return encoded_jwt