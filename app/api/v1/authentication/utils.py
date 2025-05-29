from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from fastapi.responses import Response

from models import User, OTP, Purpose
from .shemas import LoginSchema, VerifySchema, VerifyResponseSchema
from core import settings
from auth import auth_manager
from utils.security import generate_otp_code, send_otp


async def login(session: AsyncSession, login_in: LoginSchema) -> LoginSchema:
    user_result = await session.execute(
        select(User).where(User.phone == login_in.phone)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        user = User(phone=login_in.phone)
        session.add(user)
        
    valid_otp_result = await session.execute(
        select(OTP).where(
            OTP.phone_or_email == login_in.phone,
            OTP.expires_at > datetime.now(timezone.utc),
            OTP.is_used == False,
            OTP.purpose == Purpose.login
        )
    )

    valid_otp = valid_otp_result.scalar_one_or_none()

    if valid_otp:
        await session.delete(valid_otp)
    
    code = generate_otp_code()

    await send_otp(
        login_in.phone,
        code
    )

    otp = OTP(
        phone_or_email = login_in.phone,
        code = code,
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.otp_validity),
        purpose = Purpose.login
    )
    
    session.add(otp)

    await session.commit()

    return login_in


async def verify(session: AsyncSession, verify_in: VerifySchema) -> VerifyResponseSchema:
    otp_result = await session.execute(
        select(OTP).where(
            OTP.phone_or_email == verify_in.phone,
            OTP.expires_at > datetime.now(timezone.utc),
            OTP.purpose == Purpose.login,
            OTP.is_used == False,
            OTP.use_count < 5
        )
    )
    otp = otp_result.scalar_one_or_none()

    if not otp:
        raise HTTPException(status_code=400, detail=f"No valid OTP found for {verify_in.phone}")
    
    if otp.code != verify_in.code:
        otp.use_count += 1
        await session.commit()
        raise HTTPException(status_code=400, detail="Invalid code")
    user_result = await session.execute(
        select(User).where(
            User.phone == verify_in.phone
        )
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = auth_manager.generate_token(user_id = user.id)

    user.is_active = True
    otp.is_used = True
    otp.use_count += 1
    await session.commit()

    return VerifyResponseSchema(token=token)


async def logout(session: AsyncSession, user: User):
    user.is_active = False
    await session.commit()
    return Response(status_code=200, content="User successfully logged out")
