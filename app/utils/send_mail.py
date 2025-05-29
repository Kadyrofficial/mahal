import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

from core import settings


def send_email_otp(to_email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Mahal OTP Code"
    msg["From"] = settings.email.user
    msg["To"] = to_email
    msg.set_content(f"Your verification code is: {code}")
    
    try:
        with smtplib.SMTP(settings.email.host, int(settings.email.port)) as server:
            server.connect()
            server.starttls()
            server.ehlo()
            server.login(settings.email.user, settings.email.password)
            server.send_message(msg)
            server.quit()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Email couldn't be sent {e}"
        )
