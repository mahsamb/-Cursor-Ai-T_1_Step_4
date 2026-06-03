from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def get_or_create_user(session: AsyncSession, telegram_id: int, full_name: str) -> User:
    query = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = query.scalar_one_or_none()
    if user:
        return user

    user = User(telegram_id=telegram_id, full_name=full_name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
