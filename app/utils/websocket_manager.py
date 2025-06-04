import json
from fastapi import HTTPException, WebSocket


class WebsocketManager:
    def __init__(self):
        self.connection: WebSocket | None = None

    def set_connection(self, websocket: WebSocket):
        self.connection = websocket

    def clear_connection(self):
        self.connection = None

    def get_connection(self) -> WebSocket | None:
        return self.connection

    async def send_otp(self, phone: str, code: str):
        connection = self.get_connection()

        if not connection:
            # Send message to owner that there is no websocket connection
            raise HTTPException(status_code=500, detail="Websocket is not connected")
        message = {
            "phone": phone,
            "code": code
        }
        await connection.send_text(json.dumps(message))


otp_websocket = WebsocketManager()
