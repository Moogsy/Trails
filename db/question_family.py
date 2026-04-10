from typing import TYPE_CHECKING

from db.base import Base

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.questions import Question


class QuestionFamily(Base):
    __tablename__ = "questions_families"

    family: Mapped[str] = mapped_column(
        Text,
        primary_key=True
    )
    extraction_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    questions: Mapped[list["Question"]] = relationship(
        back_populates="question_family"
    )


