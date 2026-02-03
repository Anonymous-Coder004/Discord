from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import desc
from app.models.rooms import Room
from app.schemas.room import RoomCreate,RoomAccessResponse
from app.models.users import User
from app.core.security import hash_password,verify_password
from app.models.room_members import RoomMember
from app.models.messages import Message

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
    current_user,
) -> Room:
    """
    Verify room password and add user to room_members.
    """

    # ── Fetch room ──────────────────────────────
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # ── Check if user already a member (idempotent) ──
    existing_member = (
        db.query(RoomMember)
        .filter(
            RoomMember.room_id == room_id,
            RoomMember.user_id == current_user.id,
        )
        .first()
    )

    if existing_member:
        # Already joined → safe no-op
        return room

    # ── Password validation ─────────────────────
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

    # ── Insert membership ───────────────────────
    member = RoomMember(
        room_id=room.id,
        user_id=current_user.id,
    )

    db.add(member)
    db.commit()
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

def check_room_access_service(
    *,
    db: Session,
    room_id: int,
    user_id: int
) -> RoomAccessResponse:
    """
    Check whether the current user is a member of the room
    and return room metadata.
    """

    # ── Fetch room ──────────────────────────────
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # ── Check membership ────────────────────────
    is_member = (
        db.query(RoomMember)
        .filter(
            RoomMember.room_id == room_id,
            RoomMember.user_id == user_id,
        )
        .first()
        is not None
    )
    room.owner_username=room.owner.username

    # ── Return response ─────────────────────────
    return RoomAccessResponse(
        is_member=is_member,
        room=room,
    )

def leave_room_service(
    *,
    db: Session,
    room_id: int,
    current_user,
) -> None:
    """
    Remove the current user from the room_members table.
    """

    member = (
        db.query(RoomMember)
        .filter(
            RoomMember.room_id == room_id,
            RoomMember.user_id == current_user.id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a member of this room",
        )

    db.delete(member)
    db.commit()

