from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils.ws_connection_manager import manager


ws_router = APIRouter(prefix="/auth")


@ws_router.websocket(
    path="/send_otp",
)
async def send_otp(websocket: WebSocket):

    await websocket.accept()
    manager.set_connection(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.clear_connection()
