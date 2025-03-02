import json

from fastapi import Depends
from redis.asyncio import Redis

from src.app.utils.redis_dependencies import get_redis_client_ws


class RedisPubSUb:
    @staticmethod
    async def redis_subscriber(
        websocket, channel, redis: Redis = Depends(get_redis_client_ws)
    ):
        print(f"[Subscriber] Attempting to subscribe to channel: {channel}")
        pubsub = redis.pubsub()
        await pubsub.subscribe(channel)
        print(f"[Subscriber] Subscribed to channel: {channel}")

        async for message in pubsub.listen():
            print(f"[Subscriber] Message received: {message}")
            if message["type"] == "message":
                data = json.loads(message["data"])
                print(f"[Subscriber] Forwarding data to websocket: {data}")
                await websocket.send_text(json.dumps(data))
