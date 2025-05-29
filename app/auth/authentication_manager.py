import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core import settings
from models import User
from db import db_helper


security = HTTPBearer()


class AuthManager:
    token_validity = settings.TOKEN_VALIDITY
    secret_key = settings.TOKEN_SECRET_KEY
    algorithm = settings.ALGORITHM

    @classmethod
    def generate_token(cls, user_id: int) -> str:
        expiration_date = datetime.now(timezone.utc) + timedelta(days=cls.token_validity)
        payload = {
            "sub": str(user_id),
            "exp": expiration_date
        }
        token = jwt.encode(
            payload,
            cls.secret_key,
            algorithm=cls.algorithm
        )
        return token

    @classmethod
    async def check_auth(
        cls,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            user_id = payload.get("sub")
            result = await session.execute(
                select(User).where(
                    User.id == int(user_id),
                    User.is_active == True
                )
            )

            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
            
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")


auth_manager = AuthManager()
