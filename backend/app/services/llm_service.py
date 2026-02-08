# app/services/llm_service.py

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import SessionLocal
from app.models.messages import Message
from app.models.room_memory import RoomMemory
from app.models.users import User
from app.agents.runner import run_llm_from_messages
from app.agents.prompts.chat_prompts import system_chat_prompt
from app.agents.prompts.summary_prompts import summarize_prompt
import asyncio
from collections import defaultdict

room_locks = defaultdict(asyncio.Lock)


# ─────────────────────────────────────────────
# Memory Helpers
# ─────────────────────────────────────────────

async def get_room_summary(db: Session, room_id: int) -> str:
    memory = (
        db.query(RoomMemory)
        .filter(RoomMemory.room_id == room_id)
        .first()
    )
    return memory.summary if memory else ""


def fetch_last_messages_for_memory(
    db: Session,
    room_id: int,
    limit: int = 50,
):
    msgs = (
        db.query(Message)
        .filter(
            Message.room_id == room_id,
            Message.sender_type.in_(["user", "llm"]),
        )
        .order_by(desc(Message.created_at))
        .limit(limit)
        .all()
    )

    return list(reversed(msgs))


def build_conversation_context(
    summary: str,
    messages: list,
):
    conversation = []

    # Base system prompt
    conversation.append({
        "role": "system",
        "content": system_chat_prompt(),
    })

    # Add rolling summary
    if summary:
        conversation.append({
            "role": "system",
            "content": f"Conversation summary:\n{summary}",
        })

    # Add past messages with identity tagging
    for msg in messages:
        if msg.sender_type == "llm":
            conversation.append({
                "role": "assistant",
                "content": msg.content,
            })
        else:
            # msg.sender_user must exist for user messages
            username = msg.sender_user.username if msg.sender_user else "Unknown"

            conversation.append({
                "role": "user",
                "content": f"User({username}): {msg.content}",
            })

    return conversation



async def generate_new_summary(
    previous_summary: str,
    recent_messages: list,
) -> str:

    convo = []

    # Summary instruction
    convo.append({
        "role": "system",
        "content": summarize_prompt(previous_summary),
    })

    # Add recent conversation
    for msg in recent_messages:
        role = "assistant" if msg.sender_type == "llm" else "user"
        convo.append({
            "role": role,
            "content": msg.content,
        })

    convo.append({
        "role": "user",
        "content": "Provide a concise updated summary of this conversation.",
    })

    return await run_llm_from_messages(convo)


async def update_room_summary(
    db: Session,
    room_id: int,
    new_summary: str,
):
    memory = (
        db.query(RoomMemory)
        .filter(RoomMemory.room_id == room_id)
        .first()
    )

    if memory:
        memory.summary = new_summary
    else:
        memory = RoomMemory(
            room_id=room_id,
            summary=new_summary,
        )
        db.add(memory)

    db.commit()


# ─────────────────────────────────────────────
# Main Orchestrator
# ─────────────────────────────────────────────

async def handle_llm_request(
    *,
    room_id: int,
    user_id: int,
    text: str,
) -> str:

    db = SessionLocal()

    try:
        # 1️⃣ Fetch current user (for identity tagging)
        user = db.get(User, user_id)
        current_username = user.username if user else "Unknown"

        # 2️⃣ Fetch memory summary
        summary = await get_room_summary(db, room_id)

        # 3️⃣ Fetch recent non-system messages
        recent_messages = fetch_last_messages_for_memory(
            db,
            room_id,
            limit=50,
        )

        # 4️⃣ Build conversation context (with usernames)
        context = build_conversation_context(
            summary=summary,
            messages=recent_messages,
        )

        # 5️⃣ Add current user message (tagged)
        context.append({
            "role": "user",
            "content": f"User({current_username}): {text}",
        })

        # 6️⃣ Generate response
        response = await run_llm_from_messages(context)

        # 7️⃣ Fire-and-forget background summarization
        asyncio.create_task(
            maybe_update_summary_background(room_id)
        )

        return response

    finally:
        db.close()



async def maybe_update_summary_background(room_id: int):
    async with room_locks[room_id]:

        db = SessionLocal()

        try:
            total_msgs = (
                db.query(Message)
                .filter(
                    Message.room_id == room_id,
                    Message.sender_type.in_(["user", "llm"]),
                )
                .count()
            )

            if total_msgs <= 75 or total_msgs % 20 != 0:
                return

            summary = await get_room_summary(db, room_id)

            recent_messages = fetch_last_messages_for_memory(
                db,
                room_id,
                limit=50,
            )

            new_summary = await generate_new_summary(
                summary,
                recent_messages,
            )

            await update_room_summary(
                db,
                room_id,
                new_summary,
            )

        except Exception:
            import logging
            logging.exception("Background summarization failed")

        finally:
            db.close()
