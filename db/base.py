import uuid
from typing import TYPE_CHECKING

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

class Base(DeclarativeBase):
    pass

TIMESTAMP_WITH_TZ_SEC_PRECISION = TIMESTAMP(timezone=True, precision=0)

def dt_utc_now() -> datetime:
    return datetime.now(timezone.utc)

def ck_user_order(table_name: str) -> CheckConstraint:
    return CheckConstraint(
        "user_a_id < user_b_id", 
        name=f"ck_user_order_{table_name}"
    )

def uuid_mapped_column() -> MappedColumn:
    return mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

def user_uuid_mapped_column(nullable: bool = False) -> MappedColumn:
    return mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=nullable
    )
