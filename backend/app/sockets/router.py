# ws/router.py
from fastapi import FastAPI, WebSocket
from .handlers import handle_websocket_connection
from typing import Callable

def register_ws_routes(app: FastAPI):
    """
    Call this from your main app (once) to register websocket endpoints.
    Example in main.py:
      from ws.router import register_ws_routes
      register_ws_routes(app)
    """

    @app.websocket("/ws/rooms/{room_id}")
    async def websocket_room_endpoint(websocket: WebSocket, room_id: int):
        # Delegate full lifecycle to handler
        await handle_websocket_connection(websocket, room_id)
