from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.room import RoomCreate, RoomResponse,RoomDetailResponse,RoomListResponse,RoomJoinResponse,RoomJoinRequest,RoomAccessResponse,RoomLeaveResponse
from app.api.dep import get_current_user
from app.services.room_service import create_room_service,list_rooms_service,get_room_by_id_service,join_room_service,delete_room_service,check_room_access_service,leave_room_service
from app.models.users import User


router = APIRouter(
    prefix="/rooms",
    dependencies=[Depends(get_current_user)],
    tags=["rooms"]
)



@router.post(
    "",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED
)
def create_room(
    payload: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_room_service(
        db=db,
        payload=payload,
        current_user=current_user,
    )

@router.get("", response_model=list[RoomListResponse])
def list_rooms(db: Session = Depends(get_db)):
    return list_rooms_service(db)


@router.get("/{room_id}", response_model=RoomDetailResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return get_room_by_id_service(db=db, room_id=room_id)


@router.post(
    "/{room_id}/join",
    response_model=RoomJoinResponse,
    status_code=status.HTTP_200_OK,
)
def join_room(
    room_id: int,
    payload: RoomJoinRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    join_room_service(
        db=db,
        room_id=room_id,
        payload=payload,
        current_user=current_user
       
    )

    return {
        "room_id": room_id,
        "status": "joined",
    }

@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_room_service(
        db=db,
        room_id=room_id,
        current_user=current_user,
    )

@router.get(
    "/{room_id}/access",
    response_model=RoomAccessResponse,
    status_code=status.HTTP_200_OK,
)
def check_room_access(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Check whether the current user has access to a room.
    Returns membership status + room metadata.
    """
    return check_room_access_service(
        db=db,
        room_id=room_id,
        current_user=current_user,
    )

@router.delete(
    "/{room_id}/leave",
    response_model=RoomLeaveResponse,
    status_code=status.HTTP_200_OK,
)
def leave_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leave_room_service(
        db=db,
        room_id=room_id,
        current_user=current_user,
    )

    return {
        "room_id": room_id,
        "status": "left",
    }