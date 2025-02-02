from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from .config import Base
import datetime


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, autoincrement=True, primary_key=True)
    post_user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, unique=True)
    description = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    comments = relationship('Comment', back_populates='post_message')
    owner = relationship('User', back_populates='posts')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, autoincrement=True, primary_key=True)
    comment_user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='comments_user')
    post_id = Column(Integer, ForeignKey('posts.id'))
    message = Column(String)
    post_message = relationship('Post', back_populates='comments')
    created_at = Column(DateTime, default=datetime.datetime.now())