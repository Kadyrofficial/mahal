from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from .shemas import LoginSchema, VerifySchema, VerifyResponseSchema
from . import utils
from models import User
from auth import auth_manager


router = APIRouter(
    tags=["Auth🔐"],
    prefix="/auth"
)


@router.post(
    path="/login",
    summary="Login🔑",
    description="Login to the platform",
    response_model=LoginSchema
)
async def login(
    login_in: LoginSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await utils.login(session=session, login_in=login_in)


@router.post(
        path="/verify",
        summary="Verify✅",
        description="Verify identity",
        response_model=VerifyResponseSchema
)
async def verify(
    verify_in: VerifySchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await utils.verify(session=session, verify_in=verify_in)


@router.post(
    path="/logout",
    summary="Logout🔓",
    description="Logout from the platform"
)
async def logout(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(auth_manager.check_auth),
):
    return await utils.logout(
        session=session,
        user=user
    )
