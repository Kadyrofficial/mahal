from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.models import User, UserType
from .schemas import ListCustomerSchema, CustomerSchema
from app.core import settings



async def get_customers(session: AsyncSession, page: int = 1) -> ListCustomerSchema:
    limit = settings.PAGINATION_LIMIT
    offset = (page - 1) * limit

    total_result = await session.execute(
        select(func.count()).select_from(User).where(User.type == UserType.customer)
    )

    total = total_result.scalar() or 0

    result = await session.execute(
        select(User)
        .where(User.type == UserType.customer)
        .order_by(desc(User.id))
        .offset(offset)
        .limit(limit)
    )

    users = result.scalars().all()

    pages = (total + limit - 1) // limit if limit > 0 else 1

    return ListCustomerSchema(
        total=total,
        pages=pages,
        limit=limit,
        users=[CustomerSchema.model_validate(user) for user in users]
    )

