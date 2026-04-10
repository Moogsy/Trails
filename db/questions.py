import uuid
from typing import TYPE_CHECKING

from db.base import Base, uuid_mapped_column
from db.question_family import QuestionFamily

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.answer import Answer


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    question_family_id: Mapped[uuid.UUID] = mapped_column(
        Text,
        ForeignKey("questions_families.family"),
        nullable=False
    )
    question_family: Mapped[QuestionFamily] = relationship(
        back_populates="questions"
    )
    value: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    answers: Mapped[list[Answer]] = relationship(
        back_populates="question"
    )
