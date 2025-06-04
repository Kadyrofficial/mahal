from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from .schemas import LoginSchema, TokenSchema
from . import utils


router = APIRouter(
    prefix="/auth",
    tags=["Admin: Auth"]
)


@router.post(
    path="/login",
    name="Login to admin",
    description="Login to admin panel of Mahal",
    response_model=TokenSchema
)
async def login(
    login_in: LoginSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await utils.login(login_in, session)
