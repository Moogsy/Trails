from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db
from api.middleware.gate import require_access
from db import User

router = APIRouter()


@router.get("/")
async def list_matches(user: User = Depends(require_access), db: AsyncSession = Depends(get_db)):
    # TODO: return matches for current user
    raise NotImplementedError
