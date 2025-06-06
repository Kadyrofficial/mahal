from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from .schemas import LoginSchema, LoginResponseSchema
from app.models import User, UserType
from app.utils import authentication, password_manager


async def login(login_in: LoginSchema, session: AsyncSession) -> LoginResponseSchema:

    result = await session.execute(
        select(User).where(
            User.phone==login_in.phone,
            User.is_active==True,
            User.type not in [UserType.admin or UserType.super_user]
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    password = password_manager.verify_password(login_in.password, user.password)

    if not password:
        raise HTTPException(status_code=404, detail="Password does not match")

    token = authentication.generate_token(user.id)

    return LoginResponseSchema(token=token, type=user.type)
