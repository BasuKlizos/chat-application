import json
import asyncio
import logging

from fastapi import Depends
from redis.asyncio import Redis

from src.app.utils.redis_dependencies import get_redis_client_ws


class RedisPubSUb:
    @staticmethod
    async def redis_subscriber(
        websocket, channel, redis: Redis = Depends(get_redis_client_ws)
    ):
        retry_delay = 1  
        while True:
            try:
                pubsub = redis.pubsub()
                await pubsub.subscribe(channel)
                # print(f"[Subscriber] Subscribed to channel: {channel}")
                logging.info(f"[Subscriber] Subscribed to channel: {channel}")
                
                # message = await pubsub.get_message(
                #     ignore_subscribe_messages=True, timeout=1.0
                # )
                # if message:
                #     data = json.loads(message["data"])
                #     # print(f"[Subscriber] Forwarding message: {data}")
                #     logging.info(f"[Subscriber] Forwarding message: {data}")
                #     await websocket.send_text(json.dumps(data))
                #     await asyncio.sleep(0.1)

                async for message in pubsub.listen():
                    if message and message['type'] == 'message':
                        data = json.loads(message['data'])
                        await websocket.send_text(json.dumps(data))
            except Exception as e:
                # # print(f"[Subscriber Error] Redis failed: {e}")
                # logging.info(f"[Subscriber Error] Redis failed: {e}")
                # await asyncio.sleep(1)
                # return await RedisPubSUb.redis_subscriber(websocket, channel, redis)
                logging.error(f"[Redis Subscriber Error] {e}. Retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
            
            finally:
                await pubsub.unsubscribe(channel)
                # print(f"[Subscriber] Unsubscribed from: {channel}")
                logging.info(f"[Subscriber] Unsubscribed from: {channel}")
