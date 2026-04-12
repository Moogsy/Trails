import uuid
from datetime import datetime

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TSTZMULTIRANGE, Range

from db.base import Base
from db.base import (
    uuid_mapped_column, 
    user_uuid_mapped_column, 
    TIMESTAMP_WITH_TZ_SEC_PRECISION
)

class Availability(Base):
    __tablename__ = "availabilities"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    user_id: Mapped[uuid.UUID] = user_uuid_mapped_column()

    # Timestamp over that day only
    availability: Mapped[list[Range[datetime]]] = mapped_column(
        TSTZMULTIRANGE, 
        nullable=False
    )

    set_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=False
    )

    __table_args__ = (
        Index(
            "ix_availability_user_id_set_at",
            user_id,
            set_at
        ),
    )