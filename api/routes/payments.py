from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db

router = APIRouter()


@router.post("/apple/webhook")
async def apple_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    raise NotImplementedError


@router.post("/google/webhook")
async def google_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    raise NotImplementedError
