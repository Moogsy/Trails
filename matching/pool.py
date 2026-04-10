from db import *
from sqlalchemy import select, or_
from sqlalchemy.orm import Session as SQLSession

from datetime import datetime, timezone, timedelta



def get_eligible_users(db: SQLSession) -> list[User]:
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(hours=24)

    active_subq = (
        select(Subscription.id)
        .where(Subscription.user_id == User.id)
        .where(Subscription.starts_at <= now)
        .where(
            or_(
                Subscription.ends_at.is_(None),
                Subscription.ends_at > now,
            )
        )
        .exists()
    )

    recent_answer_subq = (
        select(Answer.id)
        .where(Answer.user_id == User.id)
        .where(Answer.submitted_at >= yesterday)
        .exists()
    )

    stmt = (
        select(User)
        .where(User.deleted_at.is_(None))
        .where(active_subq)
        .where(recent_answer_subq)
    )

    result = db.execute(stmt)
    as_seq = result.scalars().all()

    return list(as_seq)
