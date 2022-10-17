from ast import Pass
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import date, datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
   pass

class UserOut(BaseModel):
    email: EmailStr
    created_at: date
    class Config:
        orm_mode = True

class Post(PostBase):
    id:int
    created_at: datetime
    class Config:
        orm_mode = True
    owner_id: int
    owner: UserOut

class PostOut(PostBase):
    Post: Post
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

