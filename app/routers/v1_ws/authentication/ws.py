from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils import otp_websocket


ws_router = APIRouter(prefix="/auth")


@ws_router.websocket(path="/send_otp")
async def send_otp(websocket: WebSocket):
    await websocket.accept()
    otp_websocket.set_connection(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        otp_websocket.clear_connection()
