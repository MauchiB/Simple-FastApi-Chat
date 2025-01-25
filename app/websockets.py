from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends, Cookie
from typing import Annotated, Dict, List
from app.dependencies import get_db, get_current_user_WS
from sqlalchemy.orm import Session
from app.services.websocket_services import create_message, get_ws_chat
from app.schemas.websocket_schemas import WSout

chat_router_ws = APIRouter(prefix='/ws/chat', tags=['WebSocket'])


class SocketChat:
    def __init__(self):
        self.socket: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id):
        await websocket.accept()
        if chat_id not in self.socket:
            self.socket[chat_id] = []
            self.socket[chat_id].append(websocket)
        else:
            self.socket[chat_id].append(websocket)
    
    async def disconnect(self, websocket: WebSocket, chat_id):
        if self.socket[chat_id]:
            self.socket[chat_id].remove(websocket)
        if not self.socket[chat_id]:
            del self.socket[chat_id]
            
    
    async def send_message(self, message: WSout, chat_id):
        if chat_id in self.socket:
            for websocket in self.socket[chat_id]:
                await websocket.send_json(message.model_dump())

socket = SocketChat()
'''get chat id from url and token from cookie.'''
@chat_router_ws.websocket('/{chat_id}')
async def first(chat_id, 
                websocket: WebSocket, 
                db: Annotated[Session, Depends(get_db)],
                token: str = Cookie(),):
    user = get_current_user_WS(token=token, db=db)
    if not user:
        raise WebSocketDisconnect
    await socket.connect(websocket=websocket, chat_id=chat_id)
    try:
        while True:
            '''receive_json - {'message':message}'''
            data = await websocket.receive_json()
            chat = await get_ws_chat(db=db, user=user, chat_id=chat_id)
            if not chat:
                raise WebSocketDisconnect
            message = await create_message(db=db, user=user, chat_id=chat_id, message=data['message'])
            if message:
                await socket.send_message(message=message, chat_id=chat_id)
            else:
                await socket.disconnect(websocket=websocket, chat_id=chat_id)
    except WebSocketDisconnect:
        await socket.disconnect(websocket=websocket, chat_id=chat_id)