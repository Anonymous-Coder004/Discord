from contextvars import ContextVar

current_room_id: ContextVar[int | None] = ContextVar("current_room_id", default=None)
