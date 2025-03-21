import json
import asyncio

from fastapi import WebSocket, Depends
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
        try:
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message:
                    data = json.loads(message["data"])
                    print(f"[Subscriber] Forwarding message: {data}")
                    await WebSocket.send_text(json.dumps(data))
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[Subscriber Error] Redis failed: {e}")
