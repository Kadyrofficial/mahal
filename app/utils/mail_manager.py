import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

from app.messages import email_verification_messages
from app.core import settings


class Mail:
    def __init__(self):
        self.email = settings.EMAIL_USER
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.password = settings.EMAIL_PASS


    def send_otp(self, lang: str, to: str, code: str):
        subject = email_verification_messages[lang]["subject"]
        body = email_verification_messages[lang]["body"].format(code=code)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = to
        msg.set_content(body)
        try:
            with smtplib.SMTP(self.host, int(self.port)) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email, self.password)
                server.send_message(msg)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Email couldn't be sent: {e}")


mail = Mail()
