from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from app.models import User, OTP, Purpose
from .shemas import NameShema, PhoneShema, VerifyPhoneShema, EmailShema, VerifyEmailShema
from app.utils import generate_otp_code, otp_websocket, mail
from app.core import settings


async def update_me_name(name_in: NameShema, user: User, session: AsyncSession) -> NameShema:
    update_name = name_in.model_dump()

    for key, value in update_name.items():
        setattr(user, key, value)

    await session.commit()

    return name_in


async def update_phone(phone_in: PhoneShema, session: AsyncSession, user: User) -> PhoneShema:
    if user.phone == phone_in.phone:
        raise HTTPException(status_code=400, detail="Please enter different phone number")

    result = await session.execute(
        select(User).where(
            User.phone==phone_in.phone
        )
    )

    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=409, detail=f"User with {phone_in.phone} exists")

    code = generate_otp_code()

    await otp_websocket.send_otp(phone_in.phone, code)

    otp = OTP(
        phone_or_email=phone_in.phone,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.otp_validity),
        purpose=Purpose.change_phone
    )

    session.add(otp)
    await session.commit()

    return phone_in


async def verify_new_phone(verify_in: VerifyPhoneShema, session: AsyncSession, user: User) -> PhoneShema:
    otp_result = await session.execute(
        select(OTP).where(
            OTP.phone_or_email == verify_in.phone,
            OTP.code == verify_in.code,
            OTP.expires_at > datetime.now(timezone.utc),
            OTP.is_used == False,
            OTP.use_count < 5
        )
    )

    otp = otp_result.scalar_one_or_none()

    if otp is None:
        raise HTTPException(status_code=400, detail=f"No valid OTP found for {verify_in.phone}")

    if otp.code != verify_in.code:
        otp.use_count += 1

        await session.commit()

        raise HTTPException(status_code=400, detail="Invalid code")

    otp.is_used = True

    user.phone = verify_in.phone

    await session.commit()

    return PhoneShema(phone=verify_in.phone)


async def update_email(email_in: EmailShema, request: Request, session: AsyncSession, user: User) -> EmailShema:
    if email_in.email == user.email:
        raise HTTPException(status_code=400, detail="This is your email")

    code = generate_otp_code()

    lang = request.headers.get("accept-language", "tm")

    mail.send_otp(lang, email_in.email, code)

    otp = OTP(
        phone_or_email=email_in.email,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.otp_validity),
        purpose=Purpose.add_email
    )

    session.add(otp)
    await session.commit()

    return email_in


async def verify_new_email(verify_in: VerifyEmailShema, session: AsyncSession, user: User) -> EmailShema:
    result = await session.execute(
        select(OTP).where(
            OTP.phone_or_email == verify_in.email,
            OTP.is_used == False,
            OTP.use_count < 5,
            OTP.expires_at > datetime.now(timezone.utc),
            OTP.purpose == Purpose.add_email
        )
    )

    otp = result.scalar_one_or_none()

    if not otp:
        raise HTTPException(status_code=404, detail="Email or code is invalid")
    
    if otp.code != verify_in.code:
        otp.use_count += 1
        await session.commit()
        raise HTTPException(status_code=400, detail="Invalid code")
    
    otp.is_used = True
    user.email = verify_in.email
    await session.commit()
    return EmailShema(email=verify_in.email)
