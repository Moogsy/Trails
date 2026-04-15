from datetime import datetime, timezone
from db import AsyncSessionLocal, Match
from matching.pool import get_eligible_users
from matching.scoring import compute_score


async def run_batch() -> None:
    async with AsyncSessionLocal() as db:
        users = await get_eligible_users(db)
        batch_date = datetime.now(timezone.utc)

        for i, user_a in enumerate(users):
            for user_b in users[i + 1:]:
                score = compute_score(user_a.id, user_b.id, db)
                match = Match(
                    user_a_id=user_a.id,
                    user_b_id=user_b.id,
                    score=score,
                    batch_date=batch_date,
                )
                db.add(match)

        await db.commit()
