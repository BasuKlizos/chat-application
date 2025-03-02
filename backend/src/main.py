import psutil

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from prometheus_client import Counter, Gauge, generate_latest

from src.app.routes import websockets
from src.app.routes import auth, users, chats
from src.app.redis.conf_redis import lifespan
from src.app.utils.metrics import HTTP_REQUESTS, CPU_USAGE, MEMORY_USAGE

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


# Middleware to update HTTP metrics
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    HTTP_REQUESTS.inc()
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used / (1024 * 1024))
    response = await call_next(request)
    return response

# Expose a /metrics endpoint for Prometheus to scrape
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")