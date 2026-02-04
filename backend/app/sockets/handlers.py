# app/sockets/handlers.py

from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime, timezone
import logging

from app.db.session import SessionLocal
from app.services.room_service import check_room_access_service
from app.services.message_service import (
    save_message_best_effort,
    fetch_recent_messages,
)
from app.schemas.socket import HistoryMessagePayload
from app.sockets.manager import manager
from app.sockets.auth import get_user_id_from_ws
from app.models.users import User
from app.services.message_service import detect_llm_invoke
logger = logging.getLogger(__name__)


async def handle_websocket_connection(websocket: WebSocket, room_id: int):
    """
    FINAL STABLE WS FLOW (schema-safe):

    1. Authenticate
    2. Authorize
    3. Accept socket
    4. Send chat history (DB)
    5. Persist JOIN → broadcast via schema
    6. Persist CHAT → broadcast via schema
    7. Broadcast LEAVE → persist LEAVE
    """

    # ───────────── AUTH ─────────────
    try:
        user_id = get_user_id_from_ws(websocket)
    except Exception:
        await websocket.close(code=4401)
        return

    # ───────────── AUTHZ + USER ─────────────
    db = SessionLocal()
    try:
        access = check_room_access_service(
            db=db,
            room_id=room_id,
            user_id=user_id,
        )
        if not access.is_member:
            await websocket.close(code=4403)
            return

        user = db.get(User, user_id)
        username = user.username if user else "Unknown"
    finally:
        db.close()

    # ───────────── CONNECT ─────────────
    await manager.connect(room_id, websocket, user_id)

    # ───────────── HISTORY ─────────────
    limit_param = websocket.query_params.get("limit")
    try:
        history_limit = min(int(limit_param), 100) if limit_param else 50
    except ValueError:
        history_limit = 50

    db = SessionLocal()
    try:
        history = fetch_recent_messages(db=db, room_id=room_id, limit=history_limit)

        for msg in history:
            payload = HistoryMessagePayload(
                id=msg.id,
                room_id=msg.room_id,
                sender_type=msg.sender_type,
                sender_user_id=msg.sender_user_id,
                sender_username=(
                    msg.sender_user.username if msg.sender_user else None
                ),
                content=msg.content,
                message_type=msg.message_type,
                created_at=msg.created_at,
            )
            await manager.send_personal(websocket, payload.model_dump())
    finally:
        db.close()

    # ───────────── JOIN (persist → broadcast schema) ─────────────
    join_msg = save_message_best_effort(
        room_id=room_id,
        sender_type="system",
        sender_user_id=None,
        content=f"User {username} joined",
        message_type="system",
        timestamp=datetime.now(timezone.utc),
    )

    await manager.broadcast(
        room_id,
        HistoryMessagePayload(
            id=join_msg.id,
            room_id=join_msg.room_id,
            sender_type="system",
            sender_user_id=None,
            sender_username=None,
            content=join_msg.content,
            message_type="system",
            created_at=join_msg.created_at,
        ).model_dump(),
    )

    try:
        # ───────────── CHAT LOOP ─────────────
        while True:
            get_user_id_from_ws(websocket)  # JWT expiry guard

            data = await websocket.receive_json()
            if data.get("type") != "chat":
                continue

            text = data.get("content", "").strip()
            if not text:
                continue

            # ask service layer whether this is an llm invoke
            db = SessionLocal()
            try:
                is_llm_invoke = detect_llm_invoke(db, room_id=room_id, text=text)
            finally:
                db.close()

            message_type = "llm_invoke" if is_llm_invoke else "normal"
            msg = save_message_best_effort(
                room_id=room_id,
                sender_type="user",
                sender_user_id=user_id,
                content=text,
                message_type=message_type,
                timestamp=datetime.now(timezone.utc),
            )

            await manager.broadcast(
                room_id,
                HistoryMessagePayload(
                    id=msg.id,
                    room_id=msg.room_id,
                    sender_type="user",
                    sender_user_id=user_id,
                    sender_username=username,
                    content=msg.content,
                    message_type=msg.message_type,
                    created_at=msg.created_at,
                ).model_dump(),
            )

            if is_llm_invoke:
                bot_msg = save_message_best_effort(
                    room_id=room_id,
                    sender_type="llm",
                    sender_user_id=None,
                    content="🤖 Bot is active. LLM integration coming soon.",
                    message_type="llm_response",
                    timestamp=datetime.now(timezone.utc),
                )

                await manager.broadcast(
                    room_id,
                    HistoryMessagePayload(
                        id=bot_msg.id,
                        room_id=bot_msg.room_id,
                        sender_type="llm",
                        sender_user_id=None,
                        sender_username=None,
                        content=bot_msg.content,
                        message_type="llm_response",
                        created_at=bot_msg.created_at,
                    ).model_dump(),
                )


    except WebSocketDisconnect:
        logger.info("User %s disconnected from room %s", user_id, room_id)

    finally:
        # ───────────── LEAVE (broadcast → persist) ─────────────
        await manager.disconnect(room_id, websocket)

        leave_msg = save_message_best_effort(
            room_id=room_id,
            sender_type="system",
            sender_user_id=None,
            content=f"User {username} left",
            message_type="system",
            timestamp=datetime.now(timezone.utc),
        )

        await manager.broadcast(
            room_id,
            HistoryMessagePayload(
                id=leave_msg.id,
                room_id=leave_msg.room_id,
                sender_type="system",
                sender_user_id=None,
                sender_username=None,
                content=leave_msg.content,
                message_type="system",
                created_at=leave_msg.created_at,
            ).model_dump(),
        )
