import uuid

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import DATERANGE, DATEMULTIRANGE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base, 
    TIMESTAMP_WITH_TZ_SEC_PRECISION, 
    dt_utc_now, 
    uuid_mapped_column
)

from db.subscription import Subscription
from db.answer import Answer

if TYPE_CHECKING:
    from db.match import Match
    from db.session import Session
    from db.tree_node import TreeNode
    from db.node_weight import NodeWeight


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    oauth_provider: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )
    oauth_provider_uid: Mapped[str] = mapped_column(
        String, 
        nullable=False, 
        unique=True
    )
    phone_hash: Mapped[Optional[str]] = mapped_column(
        String, 
        nullable=True
    )
    device_hash: Mapped[Optional[str]] = mapped_column(
        String, 
        nullable=True
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION, 
        default=dt_utc_now, 
        nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION, 
        nullable=True
    )
    subscriptions: Mapped[list[Subscription]] = relationship(
        back_populates="user", 
    )
    answers: Mapped[list[Answer]] = relationship(
        back_populates="user"
    )
    matches_as_a: Mapped[list["Match"]] = relationship(
        foreign_keys="[Match.user_a_id]",
        back_populates="user_a",
    )
    matches_as_b: Mapped[list["Match"]] = relationship(
        foreign_keys="[Match.user_b_id]",
        back_populates="user_b",
    )
    sessions_as_a: Mapped[list["Session"]] = relationship(
        foreign_keys="[Session.user_a_id]",
        back_populates="user_a",
    )
    sessions_as_b: Mapped[list["Session"]] = relationship(
        foreign_keys="[Session.user_b_id]",
        back_populates="user_b",
    )

    availability_windows: Mapped[list[DATERANGE] | None] = mapped_column(
        DATEMULTIRANGE
    )
    tree_nodes: Mapped[list["TreeNode"]] = relationship(back_populates="user")
    node_weights: Mapped[list["NodeWeight"]] = relationship(back_populates="user")