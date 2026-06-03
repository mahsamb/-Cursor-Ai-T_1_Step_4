from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main_menu import main_menu_kb
from bot.states.checkout import CheckoutStates
from services.cart_service import get_user_by_telegram_id
from services.order_service import create_order_from_cart


router = Router()


@router.callback_query(F.data == "checkout:start")
async def checkout_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CheckoutStates.waiting_for_phone)
    await call.message.answer("لطفا شماره تماس خود را وارد کنید:")
    await call.answer()


@router.message(CheckoutStates.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.text.strip())
    await state.set_state(CheckoutStates.waiting_for_address)
    await message.answer("لطفا آدرس کامل خود را وارد کنید:")


@router.message(CheckoutStates.waiting_for_address)
async def get_address(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    phone = data.get("phone", "")
    address = message.text.strip()

    user = await get_user_by_telegram_id(session, message.from_user.id)
    if not user:
        await message.answer("ابتدا /start را ارسال کنید.", reply_markup=main_menu_kb())
        await state.clear()
        return

    order = await create_order_from_cart(session, user.id, phone, address)
    await state.clear()
    if not order:
        await message.answer("سبد خرید شما خالی است.", reply_markup=main_menu_kb())
        return

    await message.answer(
        "سفارش ثبت شد. درگاه پرداخت در نسخه بعد فعال می‌شود.",
        reply_markup=main_menu_kb(),
    )
