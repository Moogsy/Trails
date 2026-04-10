import uuid
from typing import TYPE_CHECKING

from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TIMESTAMP_WITH_TZ_SEC_PRECISION, uuid_mapped_column

if TYPE_CHECKING:
    from db.user import User


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False, 
        unique=True
    )
    user: Mapped[User] = relationship(back_populates="subscriptions")

    provider: Mapped[Optional[str]] = mapped_column(
        String, 
        nullable=True
    )
    provider_subscription_id: Mapped[Optional[str]] = mapped_column(
        String, 
        nullable=True
    )

    starts_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=False
    )
    ends_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=False
    )

    __table_args__ = (
        Index(
            "ix_subscriptions_user_id_start_desc",
            user_id,
            starts_at.desc()
        ),
    )
