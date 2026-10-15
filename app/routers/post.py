from fastapi import HTTPException,status,Depends,APIRouter,Response
from .. import models,schemas,outh2
from sqlalchemy import func
from .. database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session

router=APIRouter(
     prefix="/posts",
     tags=['Post']
)


@router.get("/",response_model=List[schemas.PostOut])
# @router.get("/")

def get_all_posts(db :Session = Depends(get_db),current_user=Depends(outh2.get_current_user),
                 limit:int=10,skip:int=0,search:Optional[str]=""):
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # result=db.query(models.Post,func.count(models.Vote.post_id).label("vote")).join(models.Vote,
    # models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(result)
    result=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
        # post:models.Post=result[0]
    # votes:int=result[1]
  
    
    # return [
    #     {"post": post, "votes": votes}
    #     for post, votes in result
    # ]

    return [
         {"post":post,
          "votes":vote} for post,vote in result
    ]
@router.get("/{id}",response_model=schemas.Post)
def get_one_post(id:int,db:Session =Depends(get_db),current_user=Depends(outh2.get_current_user)):
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found in database")
    if post.owner_id != current_user.id:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not allwoed request")
    
    
    return post

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.CreatePost,db:Session =Depends(get_db),current_user=Depends(outh2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user=Depends(outh2.get_current_user)):
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found in database")
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not allwoed request")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(post:schemas.CreatePost,id:int,db:Session=Depends(get_db),current_user=Depends(outh2.get_current_user)):


    post_query=db.query(models.Post).filter(models.Post.id==id)
    Post=post_query.first()
    if Post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with {id} not found in database")
    if post.owner_id != current_user.id:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not allwoed request")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"message":post_query.first()}



