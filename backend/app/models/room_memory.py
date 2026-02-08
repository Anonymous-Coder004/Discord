from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import INTEGER, TEXT, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from datetime import datetime
from typing import Optional


class RoomMemory(Base):
    __tablename__ = "room_memory"

    # One row per room
    room_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        default="",
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.utcnow,
    )

    # Relationship (one-to-one)
    room = relationship(
        "Room",
        back_populates="memory",
        uselist=False,
    )
