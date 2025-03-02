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
from src.app.utils.celery_tasks import MessageTasks

ws_routes = APIRouter()

active_connections: Dict[str, WebSocket] = {}


@ws_routes.websocket("/ws/{user_id}")
async def websocket_endpoints(
    websocket: WebSocket, user_id: str, redis: Redis = Depends(get_redis_client_ws)
):
    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"User {user_id} connected.")

    # await RedisPubSUb.redis_subscriber(websocket, f"chat:{user_id}")

    redis_channel = f"chat:{user_id}"
    subscriber_task = asyncio.create_task(
        RedisPubSUb.redis_subscriber(websocket, redis_channel, redis)
    )
    print(f"[WebSocket] Created subscriber task for channel: {redis_channel}")

    try:
        while True:
            data = await websocket.receive_text()
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

            MessageTasks.store_messages.delay(sender_id, receiver_id, message)
            print(
                f"Dispatched Celery task to store message from {sender_id} to {receiver_id}"
            )

            await Message.cache_new_message(sender_id, receiver_id, new_message, redis)

            # Publish message
            await redis.publish(
                f"chat:{receiver_id}",
                json.dumps({"sender_id": sender_id, "message": message}),
            )
            print(f"[WebSocket] Published message to channel: chat:{receiver_id}")

            # Directly send message if the receiver is online
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_text(
                    f"{sender_id}:{message}"
                )
                print(f"[WebSocket] Directly sent message to {receiver_id}")
            else:
                await websocket.send_text("User is offline.")
                print(f"[WebSocket] Receiver {receiver_id} is offline.")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        subscriber_task.cancel()
        del active_connections[user_id]
        print(f"User {user_id} disconnected.")

        await user_collections.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"is_online": False}}
        )
