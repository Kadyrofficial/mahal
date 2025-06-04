from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .schemas import ListUserSchema
from app.db import db_helper
from app.models import User
from app.utils import authentication
from . import crud


router = APIRouter(
    prefix="/users",
    tags=["Admin: Users"]
)


@router.get(
    path="",
    name="List users",
    description="List of users",
    response_model=ListUserSchema
)
async def get_users(
    page: Annotated[int, Query(description="Page number of the Users list", ge=1)]=1,
    admin_user: User = Depends(authentication.check_admin),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_users(session, page)
