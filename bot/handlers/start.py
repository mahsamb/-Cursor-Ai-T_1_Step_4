from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main_menu import main_menu_kb
from services.user_service import get_or_create_user


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession) -> None:
    await get_or_create_user(
        session=session,
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name or "کاربر",
    )
    await message.answer(
        "سلام! به فروشگاه مکمل‌های ورزشی خوش آمدید.\n"
        "از منوی زیر یک گزینه را انتخاب کنید:",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == "menu:main")
async def main_menu(call: CallbackQuery) -> None:
    await call.message.edit_text(
        "منوی اصلی فروشگاه:",
        reply_markup=main_menu_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "menu:support")
async def support(call: CallbackQuery) -> None:
    await call.message.edit_text(
        "پشتیبانی:\nبرای ارتباط با پشتیبانی به آیدی @support مراجعه کنید.",
        reply_markup=main_menu_kb(),
    )
    await call.answer()
