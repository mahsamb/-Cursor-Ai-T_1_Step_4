from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main_menu import main_menu_kb
from services.cart_service import get_user_by_telegram_id
from services.order_service import get_user_orders


router = Router()


@router.callback_query(F.data == "menu:orders")
async def show_orders(call: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user_by_telegram_id(session, call.from_user.id)
    if not user:
        await call.answer("ابتدا /start را ارسال کنید.", show_alert=True)
        return

    orders = await get_user_orders(session, user.id)
    if not orders:
        await call.message.edit_text("هنوز سفارشی ثبت نکرده‌اید.", reply_markup=main_menu_kb())
        await call.answer()
        return

    lines = ["سفارش‌های شما:"]
    for order in orders:
        lines.append(
            f"#{order.id} | مبلغ: {order.total_price:,.0f} تومان | وضعیت: {order.status}"
        )
    await call.message.edit_text("\n".join(lines), reply_markup=main_menu_kb())
    await call.answer()
