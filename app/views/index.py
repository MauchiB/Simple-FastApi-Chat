from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from pydantic import BaseModel
from app.views import templates
from typing import Annotated
from typing import List
from app.dependencies import get_db, get_current_user, is_auth
from app.services.chat_services import chat_list
from app.models.chat import Chat
from app.schemas.chat_schemas import ChatGlobalList

index_template = APIRouter(prefix='', tags=['responseHTML'])





@index_template.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, 'index.html', context={'title':'MachiWeb'})

@index_template.get('/login', response_class=HTMLResponse)
def LoginForm(request: Request, auth: Annotated[is_auth, Depends()]):
    return templates.TemplateResponse(request, 'login.html', context={'title':'Login'})

@index_template.get('/chats/', response_class=HTMLResponse)
def chat_list_global(request: Request, user: Annotated[get_current_user, Depends()], db: Annotated[get_db, Depends()]):
    chats = db.query(Chat).order_by(desc(Chat.created_at)).all()
    formatted_chats = [ChatGlobalList(chat_id=chat.id, name=chat.name, description=chat.description, created_at=chat.created_at.isoformat()) for chat in chats]
    return templates.TemplateResponse(request, 'chat_list.html', context={'title':'ChatList', 'chats':formatted_chats})

@index_template.get('/reg', response_class=HTMLResponse)
def reg(request: Request, auth: Annotated[is_auth, Depends()]):
    return templates.TemplateResponse(request, 'reg.html', context={'title':'Regestration'})

@index_template.get('/chat', response_class=HTMLResponse)
def chat(request: Request, user: Annotated[get_current_user, Depends()], db: Annotated[get_db, Depends()]):
    chats = chat_list(user=user, db=db)
    return templates.TemplateResponse(request, 'chat.html', context={'chats':chats, 'title':'Chat'})
 
@index_template.get('/chat-сreate', response_class=HTMLResponse)
def chat_create(request: Request, user: Annotated[get_current_user, Depends()], db: Annotated[get_db, Depends()]):
    chats = chat_list(user=user, db=db)
    return templates.TemplateResponse(request, 'create_chat.html', context={'chats':chats, 'title':'Chat create'})

