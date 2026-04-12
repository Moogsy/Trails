import uuid
from typing import TYPE_CHECKING, Optional

from datetime import datetime
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base,
    TIMESTAMP_WITH_TZ_SEC_PRECISION,
    uuid_mapped_column,
)

if TYPE_CHECKING:
    from db.session_participant import SessionParticipant


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    # Picked as the earliest time in the availability overlap
    scheduled_starting_time: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=False,
    )

    # Set when the first participant sends a message
    actual_starting_time: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=True,
    )

    # Set when the session ends
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=True,
    )

    participants: Mapped[list["SessionParticipant"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
