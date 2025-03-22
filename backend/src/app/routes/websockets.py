import json
import asyncio
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

ws_routes = APIRouter()
active_connections: Dict[str, List[WebSocket]] = {}
message_queue = asyncio.Queue()


async def process_message_queue():
    """Retries failed message saves in MongoDB."""
    while True:
        sender_id, receiver_id, message = await message_queue.get()
        try:
            chat_data = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message": message,
                "timestamp": datetime.now(timezone.utc),
            }
            await chat_collections.insert_one(chat_data)
            WS_DB_QUERIES.inc()
        except Exception as e:
            print(f"[DB Error] Failed to save message. Retrying... {e}")
            await asyncio.sleep(1)
            await message_queue.put((sender_id, receiver_id, message))  # Retry


async def mark_user_offline(user_id: str):
    """Marks the user as offline in MongoDB asynchronously."""
    try:
        await user_collections.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"is_online": False}}
        )
    except Exception as e:
        print(f"[MongoDB Error] Failed to update user status: {e}")


asyncio.create_task(process_message_queue())


@ws_routes.websocket("/ws/{user_id}")
async def websocket_endpoints(
    websocket: WebSocket, user_id: str, redis: Redis = Depends(get_redis_client_ws)
):
    await websocket.accept()
    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)

    WS_CONNECTIONS.inc()
    WS_TOTAL_CONNECTIONS.inc()

    print(f"User {user_id} connected.")

    redis_channel = f"chat:{user_id}"
    subscriber_task = asyncio.create_task(
        RedisPubSUb.redis_subscriber(websocket, redis_channel, redis)
    )
    print(f"[WebSocket] Created subscriber task for channel: {redis_channel}")
    REDIS_CHANNELS_CREATED.inc()
    REDIS_QUERIES_TOTAL.inc()

    try:
        while True:
            data = await websocket.receive_text()
            WS_MESSAGES_RECEIVED.inc()
            WS_MESSAGES_TOTAL.inc()

            print(f"[WebSocket] Received data: {data}")
            sender_id, receiver_id, message = data.split(":", 2)

            new_message = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message": message,
                "timestamp": datetime.now(timezone.utc),
            }

            await message_queue.put((sender_id, receiver_id, message))

            # Directly send message if the receiver is online
            if receiver_id in active_connections:
                for connection in active_connections[
                    receiver_id
                ]:  # Send to all actived connection
                    await connection.send_text(f"{sender_id}:{message}")
                WS_MESSAGES_SENT.inc()
                print(f"[WebSocket] Directly sent message to {receiver_id}")
            else:
                asyncio.create_task(
                    Message.cache_new_message(
                        sender_id, receiver_id, new_message, redis
                    )
                )
                REDIS_QUERIES_TOTAL.inc()

                asyncio.create_task(
                    redis.publish(
                        f"chat:{receiver_id}",
                        json.dumps({"sender_id": sender_id, "message": message}),
                    )
                )
                REDIS_QUERIES_TOTAL.inc()
                print(f"[WebSocket] Cached & published message to {receiver_id}")

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        subscriber_task.cancel()

        asyncio.create_task(mark_user_offline(user_id))
        active_connections.pop(user_id, None)

        print(f"User {user_id} disconnected.")

        WS_CONNECTIONS_DISC.dec()
        WS_CONNECTIONS.dec()
