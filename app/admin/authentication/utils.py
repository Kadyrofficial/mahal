from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from .schemas import LoginSchema, TokenSchema
from app.models import User
from app.utils import authentication


async def login(login_in: LoginSchema, session: AsyncSession) -> str:
    result = await session.execute(
        select(User).where(
            User.phone==login_in.phone,
            User.password==login_in.password,
            User.is_active==True
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Admin user not found")

    token = authentication.generate_token(user.id)

    return TokenSchema(token=token)
