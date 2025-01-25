from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user, get_db, join_in_chat
from typing import Annotated, List
from sqlalchemy.orm import Session
from app.models.chat import Chat, ChatUser
from app.services.chat_services import get_chat, create_chat, chat_list
from app.schemas.chat_schemas import ChatList, ChatCreate
from app.config import templates

chat_router = APIRouter(prefix='/chat', tags=['chats'])

@chat_router.get('/get-chat/{chat_id}', summary='Return html with message list', description='Returns html with a list of messages if the user is in a chat')
def chat(chat_id,
         user: Annotated[get_current_user, Depends()], 
         db: Annotated[Session, Depends(get_db)]):
    chat = get_chat(chat_id=chat_id, db=db, user=user)
    if not chat:
        raise HTTPException(status_code=404, detail={'error':'not found'})
    chat_html = templates.get_template('chatInner.html')
    html = chat_html.render(messages=chat['messages'],
                            count=chat['count'],
                            name=chat['chat_name'],
                            chat_id=chat['chat_id'],
                            username=chat['username'])
    return {'chat':html}


@chat_router.post('/chat-password', status_code=200, summary='Check user in chat', description='Checks if the user is in the chat, if not, you need a password')
def join_user_in_chat(join: Annotated[join_in_chat, Depends()]):
    if join:
        return {'ok':'ok'}
    raise HTTPException(status_code=409, detail={f'password':'incorrect password - {join}'})
    

@chat_router.get('/chat-list', response_model=List[ChatList],  summary='Return your chats')
def chats(user: Annotated[get_current_user, Depends()], 
          db: Annotated[Session, Depends(get_db)]):
    chat = chat_list(db=db, user=user)
    return chat


@chat_router.post('/chat-create', summary='Create chat', description='Creates a chat using information from the request body and the user becomes the chat admin.')
def create_chat_for_user(chat: ChatCreate, 
                         db: Annotated[Session, Depends(get_db)], 
                         user: Annotated[get_current_user, Depends()]):
    chat = create_chat(chat=chat, db=db, user=user)
    if chat:
        return None
    return HTTPException(status_code=409, detail={'error':'You can create chat 5 time'})

@chat_router.post('/logout-chat/{id}', summary='logout from chat', description='Receives an ID chat from a link, and if the user in the chat deletes it from the chat, if the chat is empty, it is also deleted.')
def logout_fromChat(id, 
                    db: Annotated[Session, Depends(get_db)], 
                    user: Annotated[get_current_user, Depends()]):
    chat = db.query(Chat).get(id)
    if chat and user in chat.users:
        delete = db.query(ChatUser).filter(ChatUser.chat_id == id, ChatUser.user_id == user.id).first()
        db.delete(delete)
        db.commit()
        remaining = db.query(ChatUser).filter(ChatUser.chat_id == id).count()
        if remaining == 0:
            db.delete(chat)
            db.commit()
        return None
    raise HTTPException(404)
     

