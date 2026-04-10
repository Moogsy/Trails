from datetime import datetime, timedelta, timezone
from jose import jwt
from config import settings

JWT_ALGORITHM = "HS256"
JWT_EXPIRY_DAYS = 30


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRY_DAYS),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=JWT_ALGORITHM)
