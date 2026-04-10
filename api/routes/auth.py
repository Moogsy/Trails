from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.deps import get_db
from api.middleware.auth import create_access_token
from db import User

router = APIRouter()


class VerifyRequest(BaseModel):
    provider: str       # "apple" | "google"
    identity_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/verify", response_model=TokenResponse)
async def verify(body: VerifyRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    # TODO: verify identity_token against Apple/Google public keys
    provider_uid = _verify_identity_token(body.provider, body.identity_token)

    result = await db.execute(
        select(User).filter_by(
            oauth_provider=body.provider,
            oauth_provider_uid=provider_uid,
        )
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(oauth_provider=body.provider, oauth_provider_uid=provider_uid)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return TokenResponse(access_token=create_access_token(str(user.id)))


def _verify_identity_token(provider: str, token: str) -> str:
    from config import settings
    if settings.env == "test":
        return token
    raise NotImplementedError
