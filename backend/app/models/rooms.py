from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from datetime import datetime
from app.db.base import Base
from typing import Optional
class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    has_llm: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false")
    )

    llm_username: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
    __table_args__ = (
        CheckConstraint(
            """
            (has_llm = false AND llm_username IS NULL)
            OR
            (has_llm = true AND llm_username IS NOT NULL)
            """,
            name="llm_username_check"
        ),
    )
    owner = relationship(
        "User",
        backref="owned_rooms",
        lazy="joined"
    )
    messages = relationship(
        "Message",
        back_populates="room",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    memory: Mapped[Optional["RoomMemory"]] = relationship(
        "RoomMemory",
        back_populates="room",
        uselist=False,
        cascade="all, delete-orphan",
    )
    document: Mapped[Optional["RoomDocument"]] = relationship(
        "RoomDocument",
        back_populates="room",
        uselist=False,  # 1 room = 1 pdf
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


