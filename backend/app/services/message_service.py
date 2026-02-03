# app/sockets/message_service.py

"""
Best-effort message persistence for WebSocket messages.

This helper:
- Matches the Message model exactly
- Never crashes the WebSocket loop
- Logs failures instead of raising
"""

import logging
from typing import Optional
from datetime import datetime
from app.models.messages import Message
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.models.messages import Message
from app.models.rooms import Room
logger = logging.getLogger(__name__)


def save_message_best_effort(
    *,
    room_id: int,
    sender_type: str,
    sender_user_id: int | None,
    content: str,
    message_type: str,
    timestamp: datetime,
    reply_to_message_id: int | None = None,
):
    try:
        session = SessionLocal()
        try:
            room_exists=(
                session.query(Room.id).filter(Room.id==room_id).first()
            )
            if not room_exists:
                return None
            msg = Message(
                room_id=room_id,
                sender_type=sender_type,
                sender_user_id=sender_user_id,
                content=content,
                message_type=message_type,
                reply_to_message_id=reply_to_message_id,
                created_at=timestamp,
            )
            session.add(msg)
            session.commit()
            session.refresh(msg)
            return msg
        finally:
            session.close()
    except Exception:
        logger.exception("Message persistence failed (non-fatal)")
        return None

def fetch_recent_messages(
    db: Session,
    *,
    room_id: int,
    limit: int,
):
    """
    Fetch last N messages for a room (oldest → newest).
    """
    msgs = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
        .all()
    )

    # reverse so client receives chronological order
    return list(reversed(msgs))
