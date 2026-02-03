# app/sockets/auth.py

from typing import Optional
from fastapi import WebSocket
from app.core.security import verify_access_token
import logging

logger = logging.getLogger(__name__)


def _extract_token_from_ws(websocket: WebSocket) -> Optional[str]:
    token = websocket.query_params.get("token")
    if token:
        return token

    auth = websocket.headers.get("authorization") or websocket.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()

    return None


def get_user_id_from_ws(websocket: WebSocket) -> int:
    """
    Decode JWT from websocket and return user_id (int).
    Raises ValueError if missing / invalid / expired.
    """
    token = _extract_token_from_ws(websocket)
    if not token:
        raise ValueError("Missing token")

    try:
        payload = verify_access_token(token)  # must validate exp internally
    except Exception:
        logger.warning("WebSocket token verification failed")
        raise ValueError("Invalid token")

    sub = payload.get("sub")
    if sub is None:
        raise ValueError("Token missing subject")

    try:
        return int(sub)
    except Exception:
        raise ValueError("Invalid subject in token")
