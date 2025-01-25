from pydantic import BaseModel
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime


class ChatCommentList(BaseModel):
    you: Literal[True, False]
    username: str
    created_at: datetime
    message: str


class ChatCreate(BaseModel):
    name: str
    description: str
    password: str

class ChatList(BaseModel):
    chat_id: int
    name: str
    created_at: Optional[datetime]

class CreateUserInChat(BaseModel):
    chat_id: int
    password: str

class ChatGlobalList(BaseModel):
    chat_id: int
    name: str
    description: str
    created_at: str

    



