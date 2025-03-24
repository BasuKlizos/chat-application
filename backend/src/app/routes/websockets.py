import json
import asyncio
import logging
from datetime import datetime, timezone


from fastapi import WebSocket, APIRouter, Depends
from typing import Dict, List
from bson.objectid import ObjectId
from redis.asyncio import Redis

from src.database import user_collections, chat_collections
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

logging.basicConfig(level=logging.INFO)
ws_routes = APIRouter()
active_connections: Dict[str, List[WebSocket]] = {}
message_queue = asyncio.Queue()
size_batch = 100


async def batch_messages_insert():
    """Inserts messages in MongoDB in bulk instead of one-by-one."""
    while True:
        messages = []

        while len(messages) < size_batch and not message_queue.empty():
            sender_id, receiver_id, message = await message_queue.get()
            messages.append(
                {
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "message": message,
                    "timestamp": datetime.now(timezone.utc),
                }
            )

        if messages:
            try:
                await chat_collections.insert_many(messages)
                WS_DB_QUERIES.inc(len(messages))
            except Exception as e:
                logging.error(f"[DB Error] Batch message save failed: {e}")
                # Re-add messages to the queue on failure
                for msg in messages:
                    message_queue.put_nowait(
                        (msg["sender_id"], msg["receiver_id"], msg["message"])
                    )

        await asyncio.sleep(0.01)


async def mark_user_offline(user_id: str):
    """Marks the user as offline in MongoDB asynchronously."""
    try:
        await user_collections.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"is_online": False}}
        )
    except Exception as e:
        logging.error(f"[MongoDB Error] Failed to update user status: {e}")


asyncio.create_task(batch_messages_insert())


@ws_routes.websocket("/ws/{user_id}")
async def websocket_endpoints(
    websocket: WebSocket, user_id: str, redis: Redis = Depends(get_redis_client_ws)
):
    await websocket.accept()
    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)
    # active_connections.setdefault(user_id, []).append(websocket)

    WS_CONNECTIONS.inc()
    WS_TOTAL_CONNECTIONS.inc()

    # print(f"User {user_id} connected.")
    logging.info(f"User {user_id} connected.")

    redis_channel = f"chat:{user_id}"
    subscriber_task = asyncio.create_task(
        RedisPubSUb.redis_subscriber(websocket, redis_channel, redis)
    )
    # print(f"[WebSocket] Created subscriber task for channel: {redis_channel}")
    logging.info(f"[WebSocket] Created subscriber task for channel: {redis_channel}")
    REDIS_CHANNELS_CREATED.inc()
    REDIS_QUERIES_TOTAL.inc()

    try:
        while True:
            data = await websocket.receive_text()
            WS_MESSAGES_RECEIVED.inc()
            WS_MESSAGES_TOTAL.inc()

            # print(f"[WebSocket] Received data: {data}")
            logging.info(f"[WebSocket] Received data: {data}")
            sender_id, receiver_id, message = data.split(":", 2)

            new_message = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message": message,
                "timestamp": datetime.now(timezone.utc),
            }

            await message_queue.put((sender_id, receiver_id, message))
            # asyncio.create_task(message_queue.put((sender_id, receiver_id, message)))
            # message_queue.put_nowait((sender_id, receiver_id, message))

            # Directly send message if the receiver is online
            if receiver_id in active_connections:
                for connection in active_connections[
                    receiver_id
                ]:  # Send to all actived connection
                    await connection.send_text(f"{sender_id}:{message}")
                WS_MESSAGES_SENT.inc()
                # print(f"[WebSocket] Directly sent message to {receiver_id}")
                logging.info(f"[WebSocket] Directly sent message to {receiver_id}")
            # connections = active_connections.get(receiver_id)
            # if connections:
            #     for connection in connections:
            #         await connection.send_text(f"{sender_id}:{message}")
            #     WS_MESSAGES_SENT.inc()
            #     logging.info(f"[WebSocket] Directly Sent message to {receiver_id}")
            
            else:
                asyncio.create_task(
                    Message.cache_new_message(
                        sender_id, receiver_id, new_message, redis
                    )
                )

                asyncio.create_task(
                    redis.publish(
                        f"chat:{receiver_id}",
                        json.dumps({"sender_id": sender_id, "message": message}),
                    )
                )
                # await asyncio.gather(
                #     Message.cache_new_message(
                #         sender_id, receiver_id, new_message, redis
                #     ),
                #     redis.publish(
                #         f"chat:{receiver_id}",
                #         json.dumps({"sender_id": sender_id, "message": message}),
                #     ),
                # )
                REDIS_QUERIES_TOTAL.inc(2)
                # print(f"[WebSocket] Cached & published message to {receiver_id}")
                logging.info(f"[WebSocket] Cached & published message to {receiver_id}")

    except Exception as e:
        # print(f"WebSocket error: {e}")
        logging.error(f"WebSocket error: {e}")
    finally:
        subscriber_task.cancel()

        asyncio.create_task(mark_user_offline(user_id))
        active_connections.pop(user_id, None)
        # asyncio.create_task(asyncio.to_thread(active_connections.pop, user_id, None))
        # await asyncio.gather(
        #     mark_user_offline(user_id),
        #     asyncio.to_thread(active_connections.pop, user_id, None),
        # )

        # print(f"User {user_id} disconnected.")
        logging.info(f"User {user_id} disconnected.")

        WS_CONNECTIONS_DISC.dec()
        WS_CONNECTIONS.dec()
