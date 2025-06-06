from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .schemas import ListCustomerSchema
from app.db import db_helper
from app.models import User
from app.utils import authentication
from . import crud


router = APIRouter(
    prefix="/customers",
    tags=["Admin: Customers"]
)


@router.get(
    path="",
    summary="Customers list",
    response_model=ListCustomerSchema
)
async def get_customers(
    page: Annotated[int, Query(description="Page number of the Users list", ge=1)]=1,
    admin_user: User = Depends(authentication.admin_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_customers(session, page)
