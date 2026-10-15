from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import Depends,status,HTTPException
from fastapi.security  import OAuth2PasswordBearer
from sqlalchemy.orm import session
from . import schemas,database,models
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme=OAuth2PasswordBearer("login")


def create_access_token(data:dict):
    to_encode=data.copy()
    expiray_token=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp']=expiray_token
    access_token=jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return access_token


def verify_access_token(token:str,credential_exception):
    try:

        paylpad_data=jwt.decode(token,SECRET_KEY,ALGORITHM)
        id:str=paylpad_data.get("user_id")
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token:str=Depends(oauth2_scheme),db:session=Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail=f"couldnot validate credential",
                                       headers={"www-Authenticate":"Bearer"})
    token_data=verify_access_token(token,credential_exception)
    current_user=db.query(models.User).filter(models.User.id==token_data.id).first()

    return current_user