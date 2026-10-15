from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,outh2   


router=APIRouter(
    prefix="/login",
    tags=['login']
    )


@router.post("/",response_model=schemas.Token)
def login(user_credential:schemas.UserLogin,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credential.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credential")
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail=f"invalid credential")
    access_token=outh2.create_access_token({"user_id":user.id})

    return {'token':access_token,"token_type":"bearer"}

