from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional




class PostCreate(BaseModel):
    post_user_id: Optional[int]
    title: str = Field(default='My post is empty', max_length=20)
    description: str = Field(default='My post is empty', max_length=100)

class PostList(BaseModel):
    title: str
    description: str
    username: str
    email: str

class CommentList(BaseModel):
    created_at: datetime
    message: str
    username: str

class CommentCreate(BaseModel):
    comment_user_id: Optional[int]
    post_id: Optional[int]
    message: str

