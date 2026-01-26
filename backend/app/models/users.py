from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import INTEGER,String,Boolean,TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import text
from datetime import datetime
from typing import List

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(INTEGER,primary_key=True,nullable=False)
    email: Mapped[str]=mapped_column(String(255),nullable=False,unique=True)
    hashed_password: Mapped[str]=mapped_column(String(255),nullable=False)
    username:Mapped[str]=mapped_column(String(50),nullable=False,unique=True)
    created_at: Mapped[datetime]=mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')) 