from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.admin import (
    admin_main_kb,
    admin_order_detail_kb,
    admin_orders_kb,
    admin_stock_kb,
)
from config import settings
from services.admin_service import (
    change_product_stock,
    get_order_with_details,
    get_orders_paged,
    get_products_paged,
    update_order_status,
)


router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("admin"))
async def admin_panel(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("شما دسترسی ادمین ندارید.")
        return
    await message.answer("پنل مدیریت:", reply_markup=admin_main_kb())


@router.callback_query(F.data == "admin:panel")
async def admin_panel_callback(call: CallbackQuery) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("دسترسی ندارید.", show_alert=True)
        return
    await call.message.edit_text("پنل مدیریت:", reply_markup=admin_main_kb())
    await call.answer()


@router.callback_query(F.data.startswith("admin:stock:"))
async def admin_stock(call: CallbackQuery, session: AsyncSession) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("دسترسی ندارید.", show_alert=True)
        return
    page = int(call.data.split(":")[2])
    products, total = await get_products_paged(session, page, page_size=6)
    if not products and page > 0:
        products, total = await get_products_paged(session, 0, page_size=6)
        page = 0
    max_page = (total - 1) // 6 if total else 0

    lines = ["مدیریت موجودی محصولات:"]
    for p in products:
        lines.append(f"{p.name} | موجودی: {p.stock}")
    text = "\n".join(lines) if products else "محصولی یافت نشد."

    await call.message.edit_text(text, reply_markup=admin_stock_kb(products, page, max_page))
    await call.answer()


@router.callback_query(F.data.startswith("admin:stk:"))
async def admin_change_stock(call: CallbackQuery, session: AsyncSession) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("دسترسی ندارید.", show_alert=True)
        return
    _, _, _, product_id, delta, page = call.data.split(":")
    success, msg = await change_product_stock(session, int(product_id), int(delta))
    if not success:
        await call.answer(msg, show_alert=True)
        return

    products, total = await get_products_paged(session, int(page), page_size=6)
    max_page = (total - 1) // 6 if total else 0
    lines = ["مدیریت موجودی محصولات:"]
    for p in products:
        lines.append(f"{p.name} | موجودی: {p.stock}")
    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=admin_stock_kb(products, int(page), max_page),
    )
    await call.answer(msg)


@router.callback_query(F.data.startswith("admin:orders:"))
async def admin_orders(call: CallbackQuery, session: AsyncSession) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("دسترسی ندارید.", show_alert=True)
        return
    page = int(call.data.split(":")[2])
    orders, total = await get_orders_paged(session, page, page_size=6)
    if not orders and page > 0:
        orders, total = await get_orders_paged(session, 0, page_size=6)
        page = 0
    max_page = (total - 1) // 6 if total else 0

    lines = ["مدیریت وضعیت سفارش‌ها:"]
    for o in orders:
        lines.append(f"#{o.id} | {o.total_price:,.0f} تومان | {o.status}")
    text = "\n".join(lines) if orders else "سفارشی برای مدیریت وجود ندارد."

    await call.message.edit_text(text, reply_markup=admin_orders_kb(orders, page, max_page))
    await call.answer()


@router.callback_query(F.data.startswith("admin:ord:"))
async def admin_update_order(call: CallbackQuery, session: AsyncSession) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("دسترسی ندارید.", show_alert=True)
        return
    _, _, _, order_id, status, page = call.data.split(":")
    success, msg = await update_order_status(session, int(order_id), status)
    if not success:
        await call.answer(msg, show_alert=True)
        return

    orders, total = await get_orders_paged(session, int(page), page_size=6)
    max_page = (total - 1) // 6 if total else 0
    lines = ["مدیریت وضعیت سفارش‌ها:"]
    for o in orders:
        lines.append(f"#{o.id} | {o.total_price:,.0f} تومان | {o.status}")
    await call.message.edit_text(
        "\n".join(lines) if orders else "سفارشی برای مدیریت وجود ندارد.",
        reply_markup=admin_orders_kb(orders, int(page), max_page),
    )
    await call.answer(msg)


@router.callback_query(F.data.startswith("admin:od:"))
async def admin_order_details(call: CallbackQuery, session: AsyncSession) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("دسترسی ندارید.", show_alert=True)
        return
    _, _, _, order_id, page = call.data.split(":")
    order = await get_order_with_details(session, int(order_id))
    if not order:
        await call.answer("سفارش یافت نشد.", show_alert=True)
        return

    lines = [
        f"جزئیات سفارش #{order.id}",
        f"وضعیت: {order.status}",
        f"مبلغ کل: {order.total_price:,.0f} تومان",
        f"نام خریدار: {order.user.full_name}",
        f"شماره تماس: {order.phone}",
        f"آدرس: {order.address}",
        "",
        "اقلام سفارش:",
    ]
    for idx, item in enumerate(order.items, start=1):
        subtotal = item.quantity * item.price
        lines.append(
            f"{idx}) {item.product.name} | تعداد: {item.quantity} | "
            f"قیمت واحد: {item.price:,.0f} | جمع: {subtotal:,.0f} تومان"
        )

    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=admin_order_detail_kb(order.id, int(page)),
    )
    await call.answer()


@router.callback_query(F.data == "admin:noop")
async def admin_noop(call: CallbackQuery) -> None:
    await call.answer()
