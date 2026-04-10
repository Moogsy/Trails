import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Index, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base, 
    dt_utc_now,
    user_uuid_mapped_column,
    uuid_mapped_column,
    TIMESTAMP_WITH_TZ_SEC_PRECISION, 
)
from db.questions import Question

if TYPE_CHECKING:
    from db.user import User


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    user_id: Mapped[uuid.UUID] = user_uuid_mapped_column()
    user: Mapped[User] = relationship(back_populates="answers")

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False
    )
    question: Mapped[Question] = relationship(
        back_populates="answers"
    )

    value: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    submitted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION, 
        default=dt_utc_now, 
        nullable=False
    )
    __table_args__ = (
        Index(
            "ix_answers_author_created_submitted_at_desc",
            user_id,
            submitted_at.desc()
        ),
    )
