from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# title str, content str
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    class Config:
        from_attributes = True

class UserGet(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True 

class PostJoinVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class VoteDirection(int, Enum):
    downvote = 0
    upvote = 1

class Vote(BaseModel):
    post_id: int
    vote_dir: VoteDirection


class VoteOut(BaseModel):
    post_id: int
    vote_dir: int
    user: UserOut
    post: Post
    class Config:
        from_attributes = True 