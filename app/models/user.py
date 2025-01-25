from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from .config import Base
import datetime



 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hash_password= Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    posts = relationship('Post', back_populates='owner')
    chats = relationship('Chat', secondary='chat_users', back_populates='users')
    comments_user = relationship('Comment', back_populates='user')

    