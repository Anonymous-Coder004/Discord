# app/models/room_document.py

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from datetime import datetime
from app.db.base import Base
from typing import List


class RoomDocument(Base):
    __tablename__ = "room_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # 1 room = 1 pdf
        index=True
    )

    uploaded_by: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    file_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # 🔥 Store Supabase storage path instead of full URL
    storage_path: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    # Relationships
    room = relationship(
        "Room",
        back_populates="document",
        lazy="joined"
    )


    chunks: Mapped[List["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
