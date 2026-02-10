import asyncio
from datetime import datetime, timezone

from app.sockets.manager import manager
from app.db.session import SessionLocal
from app.services.rag_processor import process_pdf
from app.services.message_service import save_message_best_effort


async def start_pdf_indexing(room_id: int, user_id: int, file):

    db = SessionLocal()

    try:
        # 1️⃣ Save system message first
        msg = save_message_best_effort(
            room_id=room_id,
            sender_type="system",
            sender_user_id=None,
            content=f"Indexing started for {file.filename}",
            message_type="system",
            timestamp=datetime.now(timezone.utc),
        )

        # 2️⃣ Broadcast saved message
        if msg:
            await manager.broadcast(
                room_id,
                {
                    "id": msg.id,
                    "room_id": msg.room_id,
                    "sender_type": "system",
                    "sender_user_id": None,
                    "sender_username": None,
                    "content": msg.content,
                    "message_type": msg.message_type,
                    "created_at": msg.created_at.isoformat(),
                },
            )

        # 🚀 Run background processing
        asyncio.create_task(
            process_pdf_background(room_id, user_id, file)
        )

    finally:
        db.close()


async def process_pdf_background(room_id: int, user_id: int, file):

    db = SessionLocal()

    try:
        await process_pdf(db, room_id, user_id, file)

        # ✅ Save completion message
        msg = save_message_best_effort(
            room_id=room_id,
            sender_type="system",
            sender_user_id=None,
            content=f"Indexing completed for {file.filename}",
            message_type="system",
            timestamp=datetime.now(timezone.utc),
        )

        if msg:
            await manager.broadcast(
                room_id,
                {
                    "id": msg.id,
                    "room_id": msg.room_id,
                    "sender_type": "system",
                    "sender_user_id": None,
                    "sender_username": None,
                    "content": msg.content,
                    "message_type": msg.message_type,
                    "created_at": msg.created_at.isoformat(),
                },
            )

    except Exception as e:

        # ❌ Save failure message
        msg = save_message_best_effort(
            room_id=room_id,
            sender_type="system",
            sender_user_id=None,
            content=f"Indexing failed for {file.filename}",
            message_type="system",
            timestamp=datetime.now(timezone.utc),
        )

        if msg:
            await manager.broadcast(
                room_id,
                {
                    "id": msg.id,
                    "room_id": msg.room_id,
                    "sender_type": "system",
                    "sender_user_id": None,
                    "sender_username": None,
                    "content": msg.content,
                    "message_type": msg.message_type,
                    "created_at": msg.created_at.isoformat(),
                },
            )

    finally:
        db.close()
