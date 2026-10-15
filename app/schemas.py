from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class BasePost(BaseModel):
    title:str
    content:str
    published:bool =True
    #note this mean if valid so its be int or its none cannot be rating:int=none becouce none is not int
    #rating:Optional[int] =None

class CreatePost(BasePost):
    pass
class User(BaseModel):
    id: int
    email:str
    created_at:datetime

    class config:
        orm_mode=True

class Post(BasePost):
    id:int
    created_at:datetime
    owner_id:int
    owner:User
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    post:Post
    votes:int
      
class BaseUser(BaseModel):
    email:EmailStr
    password:str


class CreateUser(BaseUser):
    pass

class User(BaseModel):
    id: int
    email:str
    created_at:datetime

    class config:
        orm_mode=True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None


class Vote(BaseModel):
    post_id:int
    dir:int
