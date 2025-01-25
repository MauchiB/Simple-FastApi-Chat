from sqlalchemy.orm import Session
from app.models.user import User
from app.models.chat import Chat, ChatUser
from typing import List
from app.schemas.chat_schemas import ChatCommentList, ChatCreate, ChatList, CreateUserInChat


def get_chat(chat_id: int, db: Session, user: User):
    chat = db.query(Chat).get(chat_id)
    if user in chat.users:
        message = []
        for m in chat.messages:
            you = False if m.user_id != user.id else True
            message.append(ChatCommentList(you=you, username=m.user.username, created_at=m.created_at, message=m.message))
        return {'messages':message, 'count':len(message), 'chat_name':chat.name, 'chat_id':chat_id, 'username':user.username}
    return False

def create_chat(chat: ChatCreate, db: Session, user: User):
    chatic = Chat(name=chat.name, password=chat.password, owner_id=user.id, description=chat.description)
    db.add(chatic)
    db.commit()
    db.refresh(chatic)
    chats = ChatUser(user_id=user.id, chat_id=chatic.id)
    db.add(chats)
    db.commit()
    return chat

def chat_list(db: Session, user: User) -> List[ChatList]:
    user_chats = []
    for chat in user.chats:
        user_chats.append(ChatList(chat_id=chat.id, name=chat.name, created_at=chat.created_at))
    user_chats.sort(key=lambda chat_u: chat_u.created_at, reverse=True)
    return user_chats

def create_user_in_chat(db: Session, user: User, chat_data: CreateUserInChat, chat: Chat):
    if user in chat.users:
        return True
    else:
        if chat.password == chat_data.password:
            user = ChatUser(user_id=user.id, chat_id=chat.id)
            db.add(user)
            db.commit()
            db.refresh(user)
            return True
        else:
            return False 


