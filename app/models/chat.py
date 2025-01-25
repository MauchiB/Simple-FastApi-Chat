from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from .config import Base
import datetime




class ChatUser(Base):
    __tablename__ = 'chat_users'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True)

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, autoincrement=True,  primary_key=True)
    name = Column(String(20))
    description = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.now())
    password = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('User', secondary='chat_users', back_populates='chats')
    messages = relationship('Message', back_populates='chat_obj')
    owner = relationship('User', foreign_keys=[owner_id])


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, autoincrement=True, primary_key=True)
    message = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.now())
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=True)
    user = relationship('User', foreign_keys=[user_id])
    chat_obj = relationship('Chat', back_populates='messages')

