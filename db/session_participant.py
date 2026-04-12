import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base,
    TIMESTAMP_WITH_TZ_SEC_PRECISION,
    dt_utc_now,
)

if TYPE_CHECKING:
    from db.session import Session
    from db.user import User


class FlagReason(enum.Enum):
    SPAM          = "spam"
    HARASSMENT    = "harassment"
    INAPPROPRIATE = "inappropriate"
    UNDERAGE      = "underage"
    SCAM          = "scam"
    OTHER         = "other"


class SessionParticipant(Base):
    __tablename__ = "session_participants"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    session: Mapped["Session"] = relationship(back_populates="participants")

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="sessions")

    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        default=dt_utc_now,
        nullable=False,
    )
    message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # NULL means not flagged; a value means flagged with that reason
    has_flagged: Mapped[Optional[FlagReason]] = mapped_column(
        Enum(FlagReason),
        nullable=True,
    )

    __table_args__ = (
        Index("ix_session_participants_user_id", "user_id"),
    )
