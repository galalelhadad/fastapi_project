from random import randint
from sys import exception
from typing import List, Optional
from fastapi import FastAPI,Response,HTTPException,status,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.get("/")
def root():
    return {"message":"hello from FASTAPI"}


@app.get("/posts",response_model=List[schemas.Post])
def get_all_posts(db :Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts

@app.get("/posts/{id}",response_model=schemas.Post)
def get_one_post(id:int,db:Session =Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found in database")
    return post

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.CreatePost,db:Session =Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found in database")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(post:schemas.CreatePost,id:int,db:Session=Depends(get_db)):


    post_query=db.query(models.Post).filter(models.Post.id==id)
    Post=post_query.first()
    if Post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with {id} not found in database")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"message":post_query.first()}



@app.get("/users/{id}",response_model=schemas.User)
def get_user(id:int ,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found in database")
    return user
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def create_user(user:schemas.CreateUser,db:Session =Depends(get_db)):
    hash_password=utils.hash(user.password)
    user.password=hash_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


####################connect with sql quary ##########################

# while True:
    # try:

    #     conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='154012',cursor_factory=RealDictCursor)
    #     print("succesfully connect to database")
    #     break
    # except Exception as error:
    #     print("failed to connect")
    #     print("error:",error)
    #     time.sleep(3)

# @app.get("/")
# def root():
#     return {"message":"hello from FASTAPI"}

# curs=conn.cursor()
# @app.get("/posts")
# def get_all_posts():
#     curs.execute("""SELECT * FROM post """)
#     posts=curs.fetchall()
#     return posts

# @app.get("/posts/{id}")
# def get_one_post(id:int):
#     curs.execute("""SELECT * FROM post WHERE id =%s""", (id,))
#     post=curs.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with {id} not found in database")
#     return post

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_post(post:post):
#     curs.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
#     new_post=curs.fetchone()
#     conn.commit()
#     return {"new post":new_post}

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     curs.execute("""DELETE FROM post WHERE id=%s RETURNING*""",(id,))
#     conn.commit()
#     post=curs.fetchone()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with {id} not found in database")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(post:post,id:int):

#     curs.execute("""UPDATE post SET title=%s,content=%s,published=%s WHERE id =%s RETURNING * """,(post.title,post.content,post.published,id))
#     new_post=curs.fetchone()
#     conn.commit()
    
#     if new_post is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"post with {id} not found in database")
    
#     return {"message":new_post}


################# frist project with list #################33
   
# def find_post(id):
#     for post in my_post:
#         if post['id']==id:
#             return post
    
# def find_index(id):
#     for idx,post in enumerate(my_post):
#         if post['id']==id:
#             return idx

# @app.get("/posts")
# def get_all_posts():
#     return my_post

# @app.get("/posts/{id}")
# def get_one_post(id:int):
#     post=find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with {id} not found in database")
#     return post

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_post(post:post):
#     new_post=post.dict()
#     new_post['id']=randint(0,1000)
#     my_post.append(new_post)
#     return new_post

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     idx=find_index(id)
#     if idx is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with {id} not found in database")
#     my_post.pop(idx)
#     return Response(content="deleted sucseefully")

# @app.put("/posts/{id}")
# def update_post(post:post,id:int):
#     new_post=post.dict()
#     idx=find_index(id)
#     new_post['id']=id
#     if idx is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"post with {id} not found in database")
#     my_post[idx]=new_post
#     return {"message":new_post}



# OLD WAY BEFORE SCHEMA VALIDATION
# @app.post("/createpost")
# def create_post(payload:dict=Body(...)):
#     return {
#         "message":f"title :{payload['title']} and content:{payload['content']}"
#     }
# my_post=[
#     {
#         "title":"first post",
#         "content":"data in first post",
#         "id":1
#     },
#     {
#         "title":"first post",
#         "content":"data in first post",
#         "id":2
#     }
# ]

   