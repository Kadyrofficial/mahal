from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from .schemas import LoginSchema, LoginResponseSchema
from . import crud


router = APIRouter(
    prefix="/auth",
    tags=["Admin: Auth"]
)


@router.post(
    path="/login",
    summary="Login",
    response_model=LoginResponseSchema
)
async def login(
    login_in: LoginSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.login(login_in, session)
