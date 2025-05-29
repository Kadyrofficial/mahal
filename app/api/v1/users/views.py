from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from auth import auth_manager

from . import crud
from .shemas import (
    UserMeShema,
    UserMeUpdateNameShema,
    UserMeUpdatePhoneShema,
    UserMeVerifyPhoneShema,
    UserMeVerifyPhoneResponseSchema,
    UserMeUpdateEmailShema,
    UserMeVerifyEmailShema
)
from models import User


router = APIRouter(
    tags=["Users👨‍💼"],
    prefix="/users"
)


@router.get(
    path="/me",
    summary="Get the user instance🙋‍♂️",
    description="Returns the data of a user",
    response_model=UserMeShema
)
async def get_me(
    user: User = Depends(auth_manager.check_auth)
):
    return UserMeShema.model_validate(user)


@router.put(
    path="/me/name",
    summary="Update name",
    description="Update first and last name of the user",
    response_model=UserMeUpdateNameShema
)
async def update_me_name(
    name_in: UserMeUpdateNameShema,
    user: User = Depends(auth_manager.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_me_name(
        name_in=name_in,
        user=user,
        session=session
    )


@router.put(
    path="/me/phone",
    summary="Update phone number📱",
    description="Update phone number",
    response_model=UserMeUpdatePhoneShema
)
async def update_phone(
    phone_in: UserMeUpdatePhoneShema,
    user: User = Depends(auth_manager.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_phone(
        user=user,
        session=session,
        phone_in=phone_in
    )


@router.post(
        path="/me/phone/verify",
        summary="Verify updated phone number✅",
        description="Verify updated phone number",
        response_model=UserMeVerifyPhoneResponseSchema
)
async def verify_new_phone(
    verify_in: UserMeVerifyPhoneShema,
    user: User = Depends(auth_manager.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.verify_new_phone(
        verify_in=verify_in,
        user=user,
        session=session
    )


@router.put(
    path="/me/email",
    summary="Update email✉️",
    description="Update email",
    response_model=UserMeUpdateEmailShema
)
async def update_email(
    email_in: UserMeUpdateEmailShema,
    user: User = Depends(auth_manager.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_email(
        email_in=email_in,
        user=user,
        session=session
    )


@router.post(
    path="/me/email/verify",
    summary="Verify updated email✅",
    description="Verify updated email",
    response_model=UserMeUpdateEmailShema
)
async def verify_new_email(
    verify_in: UserMeVerifyEmailShema,
    user: User = Depends(auth_manager.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.verify_new_email(
        verify_in=verify_in,
        user=user,
        session=session
    )
