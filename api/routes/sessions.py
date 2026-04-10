from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db
from api.middleware.gate import require_access
from db import User

router = APIRouter()


@router.post("/")
async def join_session(user: User = Depends(require_access), db: AsyncSession = Depends(get_db)):
    # TODO: implement join_session service
    raise NotImplementedError


@router.get("/{session_id}/stream")
async def stream_session(session_id: str, user: User = Depends(require_access)):
    # SSE: subscribe to Redis channel session:<session_id>
    raise NotImplementedError


@router.post("/{session_id}/messages")
async def post_message(session_id: str, user: User = Depends(require_access), db: AsyncSession = Depends(get_db)):
    # Metadata only — content is E2E between clients
    raise NotImplementedError


@router.post("/{session_id}/typing")
async def typing_indicator(session_id: str, user: User = Depends(require_access)):
    # Pure Redis pub/sub, not persisted
    raise NotImplementedError
