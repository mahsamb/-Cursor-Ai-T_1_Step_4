from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.cart import cart_kb
from services.cart_service import (
    change_cart_item_quantity,
    get_user_by_telegram_id,
    get_user_cart,
    remove_cart_item,
)


router = Router()


def _render_cart_text(items) -> str:
    if not items:
        return "سبد خرید شما خالی است."

    lines = ["سبد خرید شما:"]
    total = 0.0
    for idx, item in enumerate(items, start=1):
        line_total = item.product.price * item.quantity
        total += line_total
        lines.append(
            f"{idx}) {item.product.name} - تعداد: {item.quantity} - {line_total:,.0f} تومان"
        )
    lines.append(f"\nمجموع: {total:,.0f} تومان")
    return "\n".join(lines)


@router.callback_query(F.data == "menu:cart")
async def show_cart(call: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user_by_telegram_id(session, call.from_user.id)
    if not user:
        await call.answer("ابتدا /start را ارسال کنید.", show_alert=True)
        return
    items = await get_user_cart(session, user.id)
    await call.message.edit_text(_render_cart_text(items), reply_markup=cart_kb(items))
    await call.answer()


@router.callback_query(F.data.startswith("rm:"))
async def remove_item(call: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user_by_telegram_id(session, call.from_user.id)
    if not user:
        await call.answer("ابتدا /start را ارسال کنید.", show_alert=True)
        return

    item_id = int(call.data.split(":")[1])
    deleted = await remove_cart_item(session, user.id, item_id)
    if not deleted:
        await call.answer("آیتم موردنظر پیدا نشد.", show_alert=True)
        return

    items = await get_user_cart(session, user.id)
    await call.message.edit_text(_render_cart_text(items), reply_markup=cart_kb(items))
    await call.answer("آیتم حذف شد.")


@router.callback_query(F.data.startswith("qty:"))
async def update_quantity(call: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user_by_telegram_id(session, call.from_user.id)
    if not user:
        await call.answer("ابتدا /start را ارسال کنید.", show_alert=True)
        return

    _, item_id, delta = call.data.split(":")
    success, msg = await change_cart_item_quantity(session, user.id, int(item_id), int(delta))
    if not success:
        await call.answer(msg, show_alert=True)
        return

    items = await get_user_cart(session, user.id)
    await call.message.edit_text(_render_cart_text(items), reply_markup=cart_kb(items))
    await call.answer(msg)


@router.callback_query(F.data == "noop")
async def noop_cart(call: CallbackQuery) -> None:
    await call.answer()
