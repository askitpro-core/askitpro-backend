from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # {room_code: [websockets]}

    async def connect(self, websocket: WebSocket, room_code: str):
        await websocket.accept()

        if room_code not in self.active_connections:
            self.active_connections[room_code] = []

        self.active_connections[room_code].append(websocket)

    async def disconnect(self, websocket: WebSocket, room_code: str):
        if room_code in self.active_connections:
            self.active_connections[room_code].remove(websocket)

            if not self.active_connections[room_code]:
                del self.active_connections[room_code]

    async def broadcast(self, room_code: str, message: str):
        for connection in self.active_connections.get(room_code, []):
            await connection.send_text(message)


manager = ConnectionManager()