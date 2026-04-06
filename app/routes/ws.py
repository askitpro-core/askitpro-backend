from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.socket_manager import manager

router = APIRouter()

@router.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await manager.connect(websocket, room_code)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_code, data)

    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_code)