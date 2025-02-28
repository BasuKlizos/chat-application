from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.app.routes import websockets
from src.app.routes import auth, users, chats
from src.app.redis.conf_redis import lifespan

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websockets.ws_routes)
app.include_router(auth.auth_routes)
app.include_router(users.user_routes)
app.include_router(chats.chat_routes)
