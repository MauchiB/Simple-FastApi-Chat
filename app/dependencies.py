from fastapi import Depends, HTTPException, Request
from app.models.config import Session as orm_session
from sqlalchemy.orm import Session as db_session
from app.security.oauth2 import get_token
import jwt
from typing import Annotated
from app.config import SECRET_KEY, ALGORITHM
from app.services.auth_services import get_user
from app.models.chat import Chat
from app.schemas.chat_schemas import CreateUserInChat
from app.services.chat_services import create_user_in_chat

def get_db():
    db = orm_session()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: Annotated[get_token, Depends()], db: Annotated[db_session, Depends(get_db)]):
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get('username')
    user = get_user(username=username, db=db)
    return user

def get_current_user_WS(token: str, db: db_session):
    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('username') 
        user = get_user(username=username, db=db)
        return user
    raise HTTPException(status_code=401, detail='User not have auth token')


def join_in_chat(chat: CreateUserInChat,
                 user: Annotated[get_current_user, Depends()],
                 db: Annotated[db_session, Depends(get_db)]):
    chat_user = db.query(Chat).get(chat.chat_id)
    if not chat_user:
        raise HTTPException(404, detail={'error':'not found chat'})
    
    chat_create_user = create_user_in_chat(db=db, user=user, chat_data=chat, chat=chat_user)
    if chat_create_user:
        return True
    return False
    
def is_auth(request: Request):
    if request.cookies.get('token'):
        raise HTTPException(status_code=404)
    

