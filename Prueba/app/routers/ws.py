from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import asyncio

router = APIRouter(tags=['ws'])

# simple in-memory connections per session
connections: Dict[str, List[WebSocket]] = {}
connections_lock = asyncio.Lock()

@router.websocket('/ws/messages/{session_id}')
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    async with connections_lock:
        connections.setdefault(session_id, []).append(websocket)
    try:
        while True:
            # keep connection alive; we don't expect messages from client in this simple design
            await websocket.receive_text()
    except WebSocketDisconnect:
        async with connections_lock:
            lst = connections.get(session_id, [])
            if websocket in lst:
                lst.remove(websocket)

async def broadcast_new_message(session_id: str, payload: dict):
    # broadcast to all connected websockets for session_id
    async with connections_lock:
        lst = list(connections.get(session_id, []))
    for ws in lst:
        try:
            await ws.send_json({'type': 'new_message', 'data': payload})
        except Exception:
            # best-effort; ignore failures
            pass
