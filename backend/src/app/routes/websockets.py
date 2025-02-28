from fastapi import WebSocket, APIRouter
from typing import Dict
from bson.objectid import ObjectId

from src.database import user_collections
from src.app.models.message_models import Message 

ws_routes = APIRouter()

active_connections: Dict[str, WebSocket] = {}


@ws_routes.websocket("/ws/{user_id}")
async def websocket_endpoints(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"User {user_id} connected.")
    try:
        while True:
            data = await websocket.receive_text()
            sender_id, receiver_id, message = data.split(":", 2)

            # Save the message in db
            await Message.save_messaage(sender_id, receiver_id, message)

            # Send message only to the intended recipient
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_text(f"{sender_id}:{message}")
            else:
                await websocket.send_text("User is offline.") 
    except:
        del active_connections[user_id]
        print(f"User {user_id} disconnected.")

        await user_collections.update_one({"_id":ObjectId(user_id)},{"$set":{"is_online":False}})
