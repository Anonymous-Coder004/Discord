# app/models/document_chunk.py

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from datetime import datetime
from app.db.base import Base
from pgvector.sqlalchemy import Vector


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("room_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_chunks: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),  # MiniLM v2 dimension
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    # Relationship
    document = relationship(
        "RoomDocument",
        back_populates="chunks",
        lazy="joined"
    )
