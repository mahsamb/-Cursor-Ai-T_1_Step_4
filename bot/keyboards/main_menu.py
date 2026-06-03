from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛍 فروشگاه", callback_data="menu:shop")],
            [InlineKeyboardButton(text="🔎 جستجو", callback_data="menu:search")],
            [InlineKeyboardButton(text="🛒 سبد خرید", callback_data="menu:cart")],
            [InlineKeyboardButton(text="📦 سفارش‌های من", callback_data="menu:orders")],
            [InlineKeyboardButton(text="💬 پشتیبانی", callback_data="menu:support")],
        ]
    )
