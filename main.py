import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.types import TelegramObject

from bot.handlers import register_handlers
from config import settings
from db.models import Base
from db.seed import seed_data, seed_sample_order
from db.session import AsyncSessionLocal, engine


class DBSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_data(session)
        await seed_sample_order(session)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    if not settings.bot_token:
        raise ValueError("BOT_TOKEN در فایل .env تنظیم نشده است.")

    await init_db()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.update.middleware(DBSessionMiddleware())
    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
