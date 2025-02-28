import json

from fastapi import WebSocket, APIRouter, Depends
from typing import Dict
from bson.objectid import ObjectId
from redis.asyncio import Redis

from src.database import user_collections
from src.app.models.message_models import Message
from src.app.utils.redis_pub_sub import RedisPubSUb
from src.app.utils.redis_dependencies import get_redis_client

ws_routes = APIRouter()

active_connections: Dict[str, WebSocket] = {}


@ws_routes.websocket("/ws/{user_id}")
async def websocket_endpoints(
    websocket: WebSocket, user_id: str, redis: Redis = Depends(get_redis_client)
):
    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"User {user_id} connected.")

    await RedisPubSUb.redis_subscriber(websocket, f"chat:{user_id}")

    try:
        while True:
            data = await websocket.receive_text()
            sender_id, receiver_id, message = data.split(":", 2)

            # Save the message in db
            await Message.save_messaage(sender_id, receiver_id, message)

            # Publish message
            redis.publish(
                f"chat:{receiver_id}",
                json.dumps({"sender_id": sender_id, "message": message}),
            )
    except:
        del active_connections[user_id]
        print(f"User {user_id} disconnected.")

        await user_collections.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"is_online": False}}
        )
