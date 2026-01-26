from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
from app.core.config import settings
from jose import JWTError,jwt
from typing import Optional
password_hash=PasswordHash.recommended() #for passowrd hashing
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes 

def hash_password(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta: Optional[timedelta] = None)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str)->dict:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #it verifies token signature using secret_key and alogrithm and if verified then returns dict
        return payload
    except JWTError as e:
        print("jwt decode error",repr(e))
        raise
    

