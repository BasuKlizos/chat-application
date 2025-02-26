from fastapi import WebSocket, APIRouter
from typing import List

ws_routes = APIRouter()

active_connections: List[WebSocket] = []


@ws_routes.websocket("/ws")
async def websocket_endpoints(websocket: WebSocket):
    await websocket.accept()
    print("------connected------")
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(data)  # Broadcast
    except:
        active_connections.remove(websocket)
