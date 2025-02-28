import json

from fastapi import Depends
from redis.asyncio import Redis

from src.app.utils.redis_dependencies import get_redis_client


class RedisPubSUb:
    @staticmethod
    async def redis_subscriber(
        websocket, channel, redis: Redis = Depends(get_redis_client)
    ):
        """Subscribe to Redis channel and send messages to WebSocket."""
        pubsub = redis.pubsub()
        pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_text(json.dumps(data))
