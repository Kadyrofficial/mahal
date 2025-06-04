from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from .shemas import LoginSchema, VerifySchema, TokenSchema
from . import crud


router = APIRouter(
    prefix="/auth",
    tags=["Auth🔐"]
)


@router.post(
    path="/login",
    summary="Login",
    description="Login to the platform",
    response_model=LoginSchema
)
async def login(
    login_in: LoginSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.login(session, login_in)


@router.post(
        path="/verify",
        summary="Verify",
        description="Verify identity",
        response_model=TokenSchema
)
async def verify(
    verify_in: VerifySchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.verify(session, verify_in)
