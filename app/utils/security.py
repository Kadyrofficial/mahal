import random
import json
from fastapi import HTTPException

from .ws_connection_manager import manager


def generate_otp_code() -> str:
    return f"{random.randint(0, 9999):04}"


async def send_otp(
    phone: str,
    code: str
):
    connection = manager.get_connection()

    if not connection:
        # Send message to owner that there is no websocket connection
        raise HTTPException(status_code=500, detail="Websocket is not connected")
    message = {
        "phone": phone,
        "code": code
    }
    await connection.send_text(json.dumps(message))
