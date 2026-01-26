from app.models.users import User
from app.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from app.core.security import verify_access_token
security=HTTPBearer(description="Paste JWT access token here")
#oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login") #Tells FastAPI that this app uses OAuth2 with Bearer tokens..token url is for docs for enabling the authorize button
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db:Session=Depends(get_db)): #fastapi calls oauth2_scheme which reads authorization header and extracts token..if header missing then 401 error
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate Credentials",headers={"WWW-Authenticate":"Bearer"})
    token=credentials.credentials
    try:
        payload = verify_access_token(token)
        raw_sub = payload.get("sub")
        user_id = int(raw_sub) if raw_sub is not None else None
        if user_id is None:
            raise credentials_exception
    except (Exception,TypeError,ValueError):
        raise credentials_exception
    user_id=int(user_id)
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise credentials_exception
    return user
        #if all good then it returns user 
