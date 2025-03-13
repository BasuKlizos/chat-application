import json
import asyncio
from datetime import datetime, timezone

from fastapi import WebSocket, APIRouter, Depends
from typing import Dict
from bson.objectid import ObjectId
from redis.asyncio import Redis

from src.database import user_collections
from src.app.models.message_models import Message
from src.app.utils.redis_pub_sub import RedisPubSUb
from src.app.utils.redis_dependencies import get_redis_client_ws
from src.app.utils.metrics import (
    WS_CONNECTIONS,
    WS_MESSAGES_RECEIVED,
    WS_MESSAGES_SENT,
    WS_DB_QUERIES,
    WS_MESSAGES_TOTAL,
    REDIS_QUERIES_TOTAL,
    REDIS_CHANNELS_CREATED,
    WS_CONNECTIONS_DISC,
    WS_TOTAL_CONNECTIONS,
)

# from src.app.utils.loki_config import ws_logger

ws_routes = APIRouter()

active_connections: Dict[str, WebSocket] = {}


@ws_routes.websocket("/ws/{user_id}")
async def websocket_endpoints(
    websocket: WebSocket, user_id: str, redis: Redis = Depends(get_redis_client_ws)
):
    await websocket.accept()
    active_connections[user_id] = websocket

    WS_CONNECTIONS.inc()
    WS_TOTAL_CONNECTIONS.inc()

    print(f"User {user_id} connected.")

    # ws_logger.info(f"WebSocket CONNECTED: User {user_id}")

    # await RedisPubSUb.redis_subscriber(websocket, f"chat:{user_id}")
    if user_id:
        redis_channel = f"chat:{user_id}"
        subscriber_task = asyncio.create_task(
            RedisPubSUb.redis_subscriber(websocket, redis_channel, redis)
        )
        print(f"[WebSocket] Created subscriber task for channel: {redis_channel}")
        REDIS_CHANNELS_CREATED.inc()
        REDIS_QUERIES_TOTAL.inc()
    # ws_logger.info(f"Subscribed to Redis channel: {redis_channel}")

    try:
        while True:
            data = await websocket.receive_text()
            if data:
                WS_MESSAGES_RECEIVED.inc()
                WS_MESSAGES_TOTAL.inc()

            # ws_logger.info(f"MESSAGE RECEIVED: {data} | From: {user_id}")

            # if data == "ping":
            #     await websocket.send_text("pong")
            #     continue

            print(f"[WebSocket] Received data: {data}")
            sender_id, receiver_id, message = data.split(":", 2)

            # await Message.save_messaage(sender_id, receiver_id, message)
            # print(f"[WebSocket] Saved message from {sender_id} to {receiver_id}")
            new_message = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message": message,
                "timestamp": datetime.now(timezone.utc),
            }

            asyncio.create_task(Message.save_messaage(sender_id, receiver_id, message))
            print("Stored message directly in MongoDB.")
            WS_DB_QUERIES.inc()
            # ws_logger.info(
            #     f"Stored message in MongoDB | From: {sender_id} → To: {receiver_id}"
            # )
            # MessageTasks.store_messages.delay(sender_id, receiver_id, message)
            # print(
            #     f"Dispatched Celery task to
            #       store message from {sender_id} to {receiver_id}"
            # )
            # try:
            #     Message.queue_message.kiq(sender_id, receiver_id, message)
            #     print(f"Message queued for {receiver_id}")
            # except ConnectionError:
            #     await Message.save_message(sender_id, receiver_id, message)
            #     print(f"Redis Down! Stored message directly in MongoDB.")

            asyncio.create_task(
                Message.cache_new_message(sender_id, receiver_id, new_message, redis)
            )
            REDIS_QUERIES_TOTAL.inc()

            # Publish message
            asyncio.create_task(redis.publish(
                f"chat:{receiver_id}",
                json.dumps({"sender_id": sender_id, "message": message}),
            )) 
            REDIS_QUERIES_TOTAL.inc()
            # ws_logger.info(f"Published message to Redis channel: chat:{receiver_id}")
            print(f"[WebSocket] Published message to channel: chat:{receiver_id}")

            # Directly send message if the receiver is online
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_text(
                    f"{sender_id}:{message}"
                )
                WS_MESSAGES_SENT.inc()
                # ws_logger.info(f"Sent message directly to {receiver_id}")
                print(f"[WebSocket] Directly sent message to {receiver_id}")
            else:
                await websocket.send_text("User is offline.")
                # ws_logger.warning(f"Receiver {receiver_id} is offline.")
                print(f"[WebSocket] Receiver {receiver_id} is offline.")
    except Exception as e:
        # ws_logger.error(f"WebSocket ERROR for User
        #                               {user_id}: {str(e)}",
        #                                               exc_info=True)
        print(f"WebSocket error: {e}")
    finally:
        subscriber_task.cancel()
        del active_connections[user_id]

        REDIS_QUERIES_TOTAL.inc()

        # ws_logger.info(f"WebSocket DISCONNECTED: User {user_id}")
        print(f"User {user_id} disconnected.")

        # if user_id not in active_connections:
        WS_CONNECTIONS_DISC.dec()
        WS_CONNECTIONS.dec()
        await user_collections.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"is_online": False}}
        )
