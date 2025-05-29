from fastapi import WebSocket


class OTPWebsocketManager:
    def __init__(self):
        self.connection: WebSocket | None = None

    def set_connection(self, websocket: WebSocket):
        self.connection = websocket

    def clear_connection(self):
        self.connection = None

    def get_connection(self) -> WebSocket | None:
        return self.connection

manager = OTPWebsocketManager()
