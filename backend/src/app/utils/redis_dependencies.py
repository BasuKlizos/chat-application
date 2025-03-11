from fastapi import WebSocket, Request
from redis.asyncio import Redis


def get_redis_client_ws(websocket: WebSocket) -> Redis:
    redis_client = websocket.app.state.redis_client
    if not redis_client:
        raise RuntimeError("Redis client is not initialized!")

    print("Redis client successfully retrieved.")
    return redis_client


def get_redis_client_http(request: Request) -> Redis:
    redis_client = request.app.state.redis_client
    if not redis_client:
        raise RuntimeError("Redis client is not initialized!")
    return redis_client
