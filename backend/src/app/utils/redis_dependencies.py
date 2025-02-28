from fastapi import WebSocket
from redis.asyncio import Redis

def get_redis_client(websocket: WebSocket) -> Redis:
    redis_client = websocket.app.state.redis_client
    if not redis_client:
        raise RuntimeError("Redis client is not initialized!")
    
    print("Redis client successfully retrieved.")
    return redis_client