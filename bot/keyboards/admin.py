from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 مدیریت موجودی", callback_data="admin:stock:0")],
            [InlineKeyboardButton(text="🧾 مدیریت سفارش‌ها", callback_data="admin:orders:0")],
            [InlineKeyboardButton(text="⬅️ منوی اصلی", callback_data="menu:main")],
        ]
    )


def admin_stock_kb(products: list, page: int, max_page: int) -> InlineKeyboardMarkup:
    rows = []
    for product in products:
        rows.append(
            [
                InlineKeyboardButton(text="➖", callback_data=f"admin:stk:{product.id}:-1:{page}"),
                InlineKeyboardButton(text=product.name[:22], callback_data="admin:noop"),
                InlineKeyboardButton(text="➕", callback_data=f"admin:stk:{product.id}:1:{page}"),
            ]
        )
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ قبلی", callback_data=f"admin:stock:{page-1}"))
    if page < max_page:
        nav_row.append(InlineKeyboardButton(text="بعدی ➡️", callback_data=f"admin:stock:{page+1}"))
    if nav_row:
        rows.append(nav_row)
    rows.append([InlineKeyboardButton(text="⬅️ پنل ادمین", callback_data="admin:panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_orders_kb(orders: list, page: int, max_page: int) -> InlineKeyboardMarkup:
    rows = []
    for order in orders:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🔍 جزئیات سفارش #{order.id}",
                    callback_data=f"admin:od:{order.id}:{page}",
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"#{order.id} پرداخت شد",
                    callback_data=f"admin:ord:{order.id}:paid:{page}",
                ),
                InlineKeyboardButton(
                    text="ارسال شد",
                    callback_data=f"admin:ord:{order.id}:shipped:{page}",
                ),
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"لغو سفارش #{order.id}",
                    callback_data=f"admin:ord:{order.id}:cancelled:{page}",
                )
            ]
        )
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ قبلی", callback_data=f"admin:orders:{page-1}"))
    if page < max_page:
        nav_row.append(InlineKeyboardButton(text="بعدی ➡️", callback_data=f"admin:orders:{page+1}"))
    if nav_row:
        rows.append(nav_row)
    rows.append([InlineKeyboardButton(text="⬅️ پنل ادمین", callback_data="admin:panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_order_detail_kb(order_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"پرداخت شد #{order_id}",
                    callback_data=f"admin:ord:{order_id}:paid:{page}",
                ),
                InlineKeyboardButton(
                    text="ارسال شد",
                    callback_data=f"admin:ord:{order_id}:shipped:{page}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"لغو سفارش #{order_id}",
                    callback_data=f"admin:ord:{order_id}:cancelled:{page}",
                )
            ],
            [InlineKeyboardButton(text="⬅️ بازگشت به سفارش‌ها", callback_data=f"admin:orders:{page}")],
        ]
    )
