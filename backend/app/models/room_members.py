from sqlalchemy import Integer, ForeignKey, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from datetime import datetime

from app.db.base import Base


class RoomMember(Base):
    __tablename__ = "room_members"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
    )

    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )

    # ─────────────────────────────────────────────
    # Relationships (optional but recommended)
    # ─────────────────────────────────────────────

    user = relationship(
        "User",
        lazy="joined",
    )

    room = relationship(
        "Room",
        lazy="joined",
    )

    # ─────────────────────────────────────────────
    # Constraints
    # ─────────────────────────────────────────────

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "user_id",
            name="uq_room_user_membership",
        ),
    )
