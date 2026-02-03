from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BaseSocketMessage(BaseModel):
    created_at: datetime


class SystemPayload(BaseSocketMessage):
    type: str = "system"
    action: str
    user_id: int
    message: str


class ChatMessagePayload(BaseSocketMessage):
    type: str = "message"
    room_id: int
    sender_type: str
    sender_user_id: Optional[int]
    sender_username: Optional[str]
    content: str
    message_type: str


class HistoryMessagePayload(BaseSocketMessage):
    type: str = "history"
    id: int
    room_id: int
    sender_type: str
    sender_user_id: Optional[int]
    sender_username: Optional[str]
    content: str
    message_type: str
    reply_to_message_id: Optional[int]
