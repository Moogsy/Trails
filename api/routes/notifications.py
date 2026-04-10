from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db
from api.middleware.gate import require_access
from db import User

router = APIRouter()


@router.post("/token")
async def register_push_token(user: User = Depends(require_access), db: AsyncSession = Depends(get_db)):
    # TODO: store Expo push token for user
    raise NotImplementedError
