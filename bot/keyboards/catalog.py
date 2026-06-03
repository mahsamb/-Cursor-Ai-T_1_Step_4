from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.models import Category, Product


def categories_kb(categories: list[Category]) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=cat.name, callback_data=f"cat:{cat.id}")] for cat in categories]
    rows.append([InlineKeyboardButton(text="⬅️ بازگشت به منو", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def products_kb(
    products: list[Product],
    category_id: int | None = None,
    page: int = 0,
    has_prev: bool = False,
    has_next: bool = False,
) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=prd.name, callback_data=f"prd:{prd.id}")] for prd in products]
    nav_row = []
    if category_id is not None and has_prev:
        nav_row.append(
            InlineKeyboardButton(text="⬅️ قبلی", callback_data=f"cat:{category_id}:p:{page-1}")
        )
    if category_id is not None and has_next:
        nav_row.append(
            InlineKeyboardButton(text="بعدی ➡️", callback_data=f"cat:{category_id}:p:{page+1}")
        )
    if nav_row:
        rows.append(nav_row)
    rows.append([InlineKeyboardButton(text="⬅️ دسته‌بندی‌ها", callback_data="menu:shop")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_detail_kb(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ افزودن به سبد", callback_data=f"add:{product_id}")],
            [InlineKeyboardButton(text="🛒 مشاهده سبد", callback_data="menu:cart")],
            [InlineKeyboardButton(text="⬅️ فروشگاه", callback_data="menu:shop")],
        ]
    )
