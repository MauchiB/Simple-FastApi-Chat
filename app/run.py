from fastapi import FastAPI
from .api.auth import auth_router
from .api.post import post_router
from .api.chat import chat_router
from app.views.index import index_template
import os
from app.websockets import chat_router_ws

app = FastAPI(debug=True,
              title='WebSocketFastApi',
              description='Simple api with fastapi. To use it, first register and log in, the token is transmitted automatically in cookies',
              version='1.0.0',
              contact={
                  'name':'Machi',
                  'email':'machibuweb@gmail.com'
              })
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(index_template)
app.include_router(chat_router_ws)
app.include_router(chat_router)

from fastapi.staticfiles import StaticFiles

static = os.path.dirname(os.path.abspath(__file__))
app.mount('/static', StaticFiles(directory=static + '/static'), name='static')

