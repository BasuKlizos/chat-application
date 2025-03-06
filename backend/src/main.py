import time
import psutil

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from prometheus_client import Counter, Gauge, generate_latest

from src.app.routes import websockets
from src.app.routes import auth, users, chats
from src.app.redis.conf_redis import lifespan
from src.app.utils.metrics import HTTP_REQUESTS, CPU_USAGE, MEMORY_USAGE, DISK_USAGE
from src.config import settings
# from src.app.utils.loki_config import root_logger
from dotenv import load_dotenv

load_dotenv(".env")

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


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    HTTP_REQUESTS.inc()  

    start_time = time.time()  # Track request duration

    
    CPU_USAGE.set(psutil.cpu_percent(interval=None))
    MEMORY_USAGE.set(psutil.virtual_memory().used / (1024 * 1024))
    DISK_USAGE.set(psutil.disk_usage("/").percent) 

    # root_logger.info(f"REQUEST: {request.method} {request.url}") 

    response = await call_next(request)
    # try:
    #     response = await call_next(request)
    # except Exception as e:
    #     root_logger.error(f"ERROR: {str(e)}", exc_info=True)
    #     raise e
    
    # Measure response time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)  # Add response time to headers

    # root_logger.info(f"RESPONSE: {response.status_code} | Time: {process_time:.4f}s")

    return response


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")