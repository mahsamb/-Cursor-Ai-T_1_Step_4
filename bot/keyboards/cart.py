from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.models import CartItem


def cart_kb(items: list[CartItem]) -> InlineKeyboardMarkup:
    rows = []
    for item in items:
        rows.append(
            [
                InlineKeyboardButton(text="➖", callback_data=f"qty:{item.id}:-1"),
                InlineKeyboardButton(text=f"{item.quantity}", callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"qty:{item.id}:1"),
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"❌ حذف {item.product.name}",
                    callback_data=f"rm:{item.id}",
                )
            ]
        )

    if items:
        rows.append([InlineKeyboardButton(text="✅ ثبت سفارش", callback_data="checkout:start")])
    rows.append([InlineKeyboardButton(text="⬅️ منوی اصلی", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
