from pydantic import BaseModel
from datetime import datetime

# title str, content str
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 


class PostCreate(PostBase):
    pass





class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 