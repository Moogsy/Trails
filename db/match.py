import enum
import uuid
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import CheckConstraint, Index, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base, 
    TIMESTAMP_WITH_TZ_SEC_PRECISION, 
    ck_user_order, 
    dt_utc_now,
    uuid_mapped_column
)

if TYPE_CHECKING:
    from db.user import User


class ScoreMethod(enum.Enum):
    COSINE = "cosine"
    LTR = "ltr"
    LIGHTFM = "lightfm"


class Match(Base):
    __tablename__ = "matches"

    # Populated initialy
    id: Mapped[uuid.UUID] = uuid_mapped_column()

    user_a_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False
    )
    user_a: Mapped[User] = relationship(
        foreign_keys=user_a_id,
        back_populates="matches_as_a"
    )


    user_b_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False
    )
    user_b: Mapped[User] = relationship(
        foreign_keys=user_b_id,
        back_populates="matches_as_b"
    )

    score: Mapped[float] = mapped_column(
        Float, 
        nullable=False
    )
    score_method: Mapped[ScoreMethod] = mapped_column(
        Enum(ScoreMethod),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION, 
        default=dt_utc_now, 
        nullable=False
    )

    __table_args__ = (
        Index(
            "ix_user_pairs_match",
            "user_a_id",
            "user_b_id"
        ),
        ck_user_order(__tablename__),
        CheckConstraint(
            "-1.0 <= score AND score <= 1.0"
        )
    )