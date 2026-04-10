import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base,
    TIMESTAMP_WITH_TZ_SEC_PRECISION,
    dt_utc_now,
    user_uuid_mapped_column,
    uuid_mapped_column,
)

if TYPE_CHECKING:
    from db.user import User
    from db.node_weight import NodeWeight


class TreeNode(Base):
    __tablename__ = "tree_nodes"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    user_id: Mapped[uuid.UUID] = user_uuid_mapped_column()
    user: Mapped["User"] = relationship(back_populates="tree_nodes")

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tree_nodes.id"),
        nullable=True,
    )
    parent: Mapped[Optional["TreeNode"]] = relationship(
        back_populates="children",
        remote_side="TreeNode.id",
    )
    children: Mapped[list["TreeNode"]] = relationship(back_populates="parent")

    label: Mapped[str] = mapped_column(Text, nullable=False)
    is_leaf: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(384), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        default=dt_utc_now,
        nullable=False,
    )

    weights: Mapped[list["NodeWeight"]] = relationship(back_populates="node")
