# app/sockets/manager.py

from fastapi import WebSocket
from typing import Dict, List
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections per room.

    _rooms = {
        room_id: [
            {
                "websocket": WebSocket,
                "user_id": int
            }
        ]
    }
    """

    def __init__(self):
        self._rooms: Dict[int, List[dict]] = {}
        self._lock = asyncio.Lock()

    # ─────────────────────────────
    # Connection lifecycle
    # ─────────────────────────────

    async def connect(self, room_id: int, websocket: WebSocket, user_id: int):
        await websocket.accept()

        async with self._lock:
            if room_id not in self._rooms:
                self._rooms[room_id] = []

            self._rooms[room_id].append(
                {
                    "websocket": websocket,
                    "user_id": user_id,
                }
            )

        logger.info("User %s connected to room %s", user_id, room_id)

    async def disconnect(self, room_id: int, websocket: WebSocket):
        async with self._lock:
            conns = self._rooms.get(room_id, [])

            self._rooms[room_id] = [
                c for c in conns if c["websocket"] is not websocket
            ]

            if not self._rooms[room_id]:
                self._rooms.pop(room_id, None)

        logger.info("WebSocket disconnected from room %s", room_id)

    # ─────────────────────────────
    # Messaging helpers
    # ─────────────────────────────

    async def send_personal(self, websocket: WebSocket, payload: dict):
        """
        Send JSON payload to a single websocket.
        """
        try:
            await websocket.send_text(json.dumps(payload, default=str))
        except Exception:
            logger.exception("Failed to send personal message")

    async def broadcast(self, room_id: int, payload: dict):
        """
        Broadcast JSON payload to all connections in a room.

        - Uses JSON serialization
        - Safe for wscat, browser, React
        """
        conns = list(self._rooms.get(room_id, []))
        if not conns:
            return

        message = json.dumps(payload, default=str)

        coros = []
        for c in conns:
            ws = c["websocket"]
            coros.append(ws.send_text(message))

        await asyncio.gather(*coros, return_exceptions=True)

    # ─────────────────────────────
    # Utilities
    # ─────────────────────────────

    def get_room_user_ids(self, room_id: int) -> List[int]:
        return [c["user_id"] for c in self._rooms.get(room_id, [])]


manager = ConnectionManager()
