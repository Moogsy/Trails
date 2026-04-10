from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status

from api.deps import get_current_user
from db import User


def require_access(user: User = Depends(get_current_user)) -> User:
    if user.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    now = datetime.now(timezone.utc)
    has_active_sub = any(
        s.starts_at <= now and (s.ends_at is None or s.ends_at >= now)
        for s in user.subscriptions
    )

    if not has_active_sub:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


def require_admin(user: User = Depends(require_access)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
