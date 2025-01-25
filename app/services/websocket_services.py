from app.models.chat import Message, Chat
from app.models.user import User
from sqlalchemy.orm import Session
from app.schemas.websocket_schemas import WSout





async def create_message(db: Session, user: User, chat_id, message: str):
    message_user = Message(user_id=user.id, chat_id=chat_id, message=message)
    db.add(message_user)
    db.commit()
    db.refresh(message_user)
    time = message_user.created_at.isoformat()
    return WSout(username=user.username, message=message_user.message, created_at=time)


async def get_ws_chat(db: Session, user: User, chat_id):
    chat = db.query(Chat).get(chat_id)
    if chat and user in chat.users:
        return True
    return False
    