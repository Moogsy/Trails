from fastapi import APIRouter, Response
from sqlalchemy import text
from db import AsyncSessionLocal
from workers import app as celery_app

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready(response: Response):
    checks = {}

    # DB check
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as e:
        checks["db"] = str(e)

    # Broker check
    try:
        pong = celery_app.control.ping(timeout=0.5)
        checks["broker"] = "ok" if pong else "no workers"
    except Exception as e:
        checks["broker"] = str(e)

    degraded = any(v != "ok" for v in checks.values())
    if degraded:
        response.status_code = 503
        return {"status": "degraded", "checks": checks}

    return {"status": "ok", "checks": checks}
