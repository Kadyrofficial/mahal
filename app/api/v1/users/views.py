from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from app.utils import authentication
from . import crud
from .shemas import MeShema, NameShema, PhoneShema, VerifyPhoneShema, EmailShema, VerifyEmailShema
from app.models import User


router = APIRouter(
    tags=["ers👨‍💼"],
    prefix="/users"
)


@router.get(
    path="/me", response_model=MeShema
)
async def get_me(
    user: User = Depends(authentication.check_auth)
):
    return MeShema.model_validate(user)


@router.put(
    path="/me/name",
    summary="Update name",
    description="Update first and last name of the user",
    response_model=NameShema
)
async def update_me_name(
    name_in: NameShema,
    user: User = Depends(authentication.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_me_name(name_in, user, session)


@router.put(
    path="/me/phone",
    summary="Update phone number📱",
    description="Update phone number",
    response_model=PhoneShema
)
async def update_phone(
    phone_in: PhoneShema,
    user: User = Depends(authentication.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_phone(phone_in, session, user)


@router.post(
        path="/me/phone/verify",
        summary="Verify updated phone number✅",
        description="Verify updated phone number"
)
async def verify_new_phone(
    verify_in: VerifyPhoneShema,
    user: User = Depends(authentication.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.verify_new_phone(verify_in, session, user)


@router.put(
    path="/me/email",
    summary="Update email✉️",
    description="Update email",
    response_model=EmailShema
)
async def update_email(
    email_in: EmailShema,
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(authentication.check_auth)
):
    return await crud.update_email(email_in, request, session, user)


@router.post(
    path="/me/email/verify",
    summary="Verify updated email✅",
    description="Verify updated email",
    response_model=EmailShema
)
async def verify_new_email(
    verify_in: VerifyEmailShema,
    user: User = Depends(authentication.check_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.verify_new_email(verify_in, session, user)
