from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    has_llm: bool = False
    llm_username: Optional[str] = Field(default=None, min_length=2, max_length=30)
    password: Optional[str] = Field(default=None, min_length=4)


class RoomResponse(BaseModel):
    id: int
    name: str
    has_llm: bool
    llm_username: Optional[str]

    class Config:
        from_attributes = True

class RoomListResponse(BaseModel):
    id: int
    name: str
    has_llm: bool
    llm_username: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RoomDetailResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    has_llm: bool
    llm_username: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class RoomJoinRequest(BaseModel):
    password: Optional[str] = Field(default=None, min_length=1)


class RoomJoinResponse(BaseModel):
    room_id: int
    status: str

class RoomAccessRoom(BaseModel):
    id: int
    name: str
    owner_id: int
    owner_username: str
    has_llm: bool
    llm_username: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RoomAccessResponse(BaseModel):
    is_member: bool
    room: RoomAccessRoom

class RoomLeaveResponse(BaseModel):
    room_id: int
    status: str