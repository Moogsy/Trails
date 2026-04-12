import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import (
    Base,
    TIMESTAMP_WITH_TZ_SEC_PRECISION,
    user_uuid_mapped_column,
    uuid_mapped_column,
)

if TYPE_CHECKING:
    from db.user import User
    from db.tree_node import TreeNode


class NodeWeight(Base):
    __tablename__ = "node_weights"

    id: Mapped[uuid.UUID] = uuid_mapped_column()

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tree_nodes.id", ondelete="CASCADE"),
        nullable=False,
    )
    node: Mapped[TreeNode] = relationship(back_populates="weights")

    user_id: Mapped[uuid.UUID] = user_uuid_mapped_column()
    user: Mapped[User] = relationship(back_populates="node_weights")

    appearances: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    recency_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    depth_factor: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    composite_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    last_updated: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP_WITH_TZ_SEC_PRECISION,
        nullable=True,
    )

    __table_args__ = (UniqueConstraint("node_id", "user_id", name="uq_node_weights_node_user"),)
