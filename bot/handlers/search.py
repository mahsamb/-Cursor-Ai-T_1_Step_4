from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.catalog import products_kb
from bot.keyboards.main_menu import main_menu_kb
from bot.states.search import SearchStates
from services.catalog_service import search_products


router = Router()


@router.callback_query(F.data == "menu:search")
async def ask_search_text(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SearchStates.waiting_for_query)
    await call.message.edit_text("لطفا نام محصول را برای جستجو وارد کنید:")
    await call.answer()


@router.message(SearchStates.waiting_for_query)
async def process_search(message: Message, state: FSMContext, session: AsyncSession) -> None:
    query = message.text.strip()
    products = await search_products(session, query)
    await state.clear()
    if not products:
        await message.answer(
            "نتیجه‌ای برای این جستجو پیدا نشد.",
            reply_markup=main_menu_kb(),
        )
        return

    await message.answer(
        "نتایج جستجو:",
        reply_markup=products_kb(products),
    )
