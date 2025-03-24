import json
import asyncio
import logging

import redis.exceptions
from fastapi import Depends, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis

from src.app.utils.redis_dependencies import get_redis_client_ws


class RedisPubSUb:
    @staticmethod
    async def redis_subscriber(
        websocket: WebSocket,
        channel,
        redis_client: Redis = Depends(get_redis_client_ws),
    ):
        a, b = 1, 1
        while True:
            try:
                pubsub = redis_client.pubsub()
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
                    if message and message["type"] == "message":
                        data = json.loads(message["data"])
                        await websocket.send_text(json.dumps(data))
            except WebSocketDisconnect:
                logging.info(
                    f"[Subscriber] WebSocket closed. Stopping listener for {channel}."
                )
                break

            except redis.exceptions.ConnectionError as e:
                logging.error(
                    f"[Redis Error] Connection lost: {e}. Retrying in {b}s..."
                )
                await asyncio.sleep(b)
                a, b = b, min(a + b, 60)

            except Exception as e:
                logging.error(f"[Unknown Error] {e}. Not retrying.")
                break

            finally:
                await pubsub.unsubscribe(channel)
                logging.info(f"[Subscriber] Unsubscribed from: {channel}")
