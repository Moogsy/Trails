import enum
import uuid
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import ForeignKey, String, Index, Integer
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base, 
    TIMESTAMP_WITH_TZ_SEC_PRECISION, 
    ck_user_order,
    dt_utc_now,
    uuid_mapped_column,
)

if TYPE_CHECKING:
    from db.user import User


class SessionStatus(enum.Enum):
    CREATED = "created"
    RUNNING = "running"
    ENDED = "ended"


class Session(Base):
    __tablename__ = "sessions"

    # Initially populated
    id: Mapped[uuid.UUID] = uuid_mapped_column()

    user_a_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False
    )
    user_a: Mapped[User] = relationship(
        foreign_keys=user_a_id,
        back_populates="sessions_as_a"
    )

    user_b_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False
    )
    user_b: Mapped[User] = relationship(
        foreign_keys=user_b_id,
        back_populates="sessions_as_b"
    )

    status: Mapped[str] = mapped_column(
        String, 
        default="active", 
        nullable=False
    )

    # Picked as the earliest time in the overlap
    scheduled_starting_time: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=False
    )

    # Set when both users sent a message
    actual_starting_time: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=False
    )

    # Populated at the end of sessions
    ended_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        default=dt_utc_now, 
        nullable=True
    )
    message_count: Mapped[int | None] = mapped_column(
        Integer, 
        default=0
    )
    user_a_message_count: Mapped[int | None] = mapped_column(
        Integer, 
        default=0
    )
    user_b_message_count: Mapped[int | None] = mapped_column(
        Integer, 
        default=0
    )

    __table_args__ = (
        ck_user_order(__tablename__),
        Index(
            "idx_sessions_pair", "user_a_id", "user_b_id",
            unique=True,
            postgresql_where="status = 'active'"
        )
    )
    





