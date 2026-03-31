from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # Maps a Room Code (e.g. "CS101") to a list of active websocket connections
        self.active_rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_code: str):
        await websocket.accept()
        if room_code not in self.active_rooms:
            self.active_rooms[room_code] = []
        self.active_rooms[room_code].append(websocket)

    def disconnect(self, websocket: WebSocket, room_code: str):
        if room_code in self.active_rooms:
            self.active_rooms[room_code].remove(websocket)
            if len(self.active_rooms[room_code]) == 0:
                del self.active_rooms[room_code]

    async def broadcast_to_room(self, message: dict, room_code: str):
        """Sends live data to everyone currently in the specified room"""
        if room_code in self.active_rooms:
            for connection in self.active_rooms[room_code]:
                await connection.send_json(message)

# Global instance to be used across all routes
manager = ConnectionManager()