from fastapi import HTTPException, Query, Response,status,Depends,APIRouter
from httpx import post
from .. import models,schemas,utils,outh2
from .. database import get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/votes",
    tags=['vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(get_db),current_user=Depends(outh2.get_current_user)):
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} not found")
    found_vote=vote_query.first()
    if vote.dir==1:

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user with id {current_user.id} voted on this post")
        else:
            new_vote=models.Vote(user_id=current_user.id,post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message":f"user with id {current_user.id} voted on post with id {vote.post_id} sucessfully"}
            
    elif vote.dir==0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {current_user.id}  not voted on this post")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
