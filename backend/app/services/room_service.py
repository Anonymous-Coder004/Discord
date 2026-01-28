from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import desc
from app.models.rooms import Room
from app.schemas.room import RoomCreate
from app.models.users import User
from app.core.security import hash_password,verify_password


def create_room_service(
    *,
    db: Session,
    payload: RoomCreate,
    current_user: User,
) -> Room:
    # ── Business validation ─────────────────────────────

    if payload.has_llm and not payload.llm_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="llm_username is required when has_llm is true",
        )

    if not payload.has_llm and payload.llm_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="llm_username must be null when has_llm is false",
        )

    # ── Hash room password if provided ──────────────────

    password_hash = None
    if payload.password:
        password_hash = hash_password(payload.password)

    # ── Create room instance ────────────────────────────

    room = Room(
        name=payload.name,
        owner_id=current_user.id,
        has_llm=payload.has_llm,
        llm_username=payload.llm_username,
        password_hash=password_hash,
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room

def list_rooms_service(db: Session) -> list[Room]:
    """
    Fetch all rooms sorted by newest first.
    Used by Home page.
    """
    rooms = (
        db.query(Room)
        .order_by(desc(Room.created_at))
        .all()
    )

    return rooms

def get_room_by_id_service(
    *,
    db: Session,
    room_id: int,
) -> Room:
    """
    Fetch a single room by ID.
    """
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    return room


def join_room_service(
    *,
    db: Session,
    room_id: int,
    payload,
) -> Room:
    """
    Verify room password and allow user to join.
    """

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # If room is protected, password is required
    if room.password_hash:
        if not payload.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room password is required",
            )

        if not verify_password(payload.password, room.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect room password",
            )

    # No membership table yet → just validation
    return room

def delete_room_service(
    *,
    db: Session,
    room_id: int,
    current_user: User,
) -> None:
    """
    Delete a room.
    Only the owner is allowed to delete the room.
    """

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the room owner can delete this room",
        )

    db.delete(room)
    db.commit()
