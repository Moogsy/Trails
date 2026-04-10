from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db
from api.middleware.gate import require_access
from db import User

router = APIRouter()


@router.post("/")
async def submit_answer(user: User = Depends(require_access), db: AsyncSession = Depends(get_db)):
    # TODO: implement submit_answer service
    raise NotImplementedError
