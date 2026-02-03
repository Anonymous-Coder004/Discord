from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    ForeignKey,
    CheckConstraint,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
    )

    # ───────────── Room ─────────────
    room_id = Column(
        BigInteger,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ───────────── Sender ─────────────
    sender_type = Column(
        String(10),
        nullable=False,
    )
    # 'user' | 'llm' | 'system'

    sender_user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ───────────── Message Content ─────────────
    content = Column(
        Text,
        nullable=False,
    )

    message_type = Column(
        String(20),
        nullable=False,
    )
    # 'normal' | 'reply' | 'llm_invoke' | 'llm_response' | 'system'

    # ───────────── Reply Metadata ─────────────
    reply_to_message_id = Column(
        BigInteger,
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ───────────── Timestamp ─────────────
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ───────────── Relationships ─────────────
    room = relationship(
        "Room",
        back_populates="messages",
    )

    sender_user = relationship("User", foreign_keys=[sender_user_id])
    replied_message = relationship("Message", remote_side=[id])

    # ───────────── Constraints ─────────────
    __table_args__ = (
        CheckConstraint(
            "sender_type IN ('user', 'llm', 'system')",
            name="check_sender_type",
        ),
        CheckConstraint(
            """
            (sender_type = 'user' AND sender_user_id IS NOT NULL)
            OR
            (sender_type = 'llm')
            OR
            (sender_type = 'system')
            """,
            name="check_sender_identity",
        ),
    )
