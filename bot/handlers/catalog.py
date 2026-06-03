from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.catalog import categories_kb, product_detail_kb, products_kb
from services.cart_service import add_to_cart, get_user_by_telegram_id
from services.catalog_service import (
    get_category_by_id,
    get_categories,
    get_product_by_id,
    get_products_by_category_paged,
)


router = Router()


@router.callback_query(F.data == "menu:shop")
async def show_categories(call: CallbackQuery, session: AsyncSession) -> None:
    categories = await get_categories(session)
    await call.message.edit_text(
        "دسته‌بندی‌ها را انتخاب کنید:",
        reply_markup=categories_kb(categories),
    )
    await call.answer()


@router.callback_query(F.data.startswith("cat:"))
async def show_products(call: CallbackQuery, session: AsyncSession) -> None:
    parts = call.data.split(":")
    category_id = int(parts[1])
    page = int(parts[3]) if len(parts) == 4 else 0
    products, total = await get_products_by_category_paged(session, category_id, page, page_size=5)
    if not products:
        await call.answer("محصولی در این دسته‌بندی موجود نیست.", show_alert=True)
        return

    category = await get_category_by_id(session, category_id)
    max_page = (total - 1) // 5 if total else 0
    await call.message.edit_text(
        f"محصولات دسته {category.name if category else ''} (صفحه {page+1} از {max_page+1}):",
        reply_markup=products_kb(
            products=products,
            category_id=category_id,
            page=page,
            has_prev=page > 0,
            has_next=page < max_page,
        ),
    )
    await call.answer()


@router.callback_query(F.data.startswith("prd:"))
async def show_product_detail(call: CallbackQuery, session: AsyncSession) -> None:
    product_id = int(call.data.split(":")[1])
    product = await get_product_by_id(session, product_id)
    if not product:
        await call.answer("محصول پیدا نشد.", show_alert=True)
        return

    text = (
        f"نام: {product.name}\n"
        f"برند: {product.brand.name}\n"
        f"قیمت: {product.price:,.0f} تومان\n"
        f"موجودی: {product.stock}\n\n"
        f"{product.description}"
    )
    await call.message.edit_text(text, reply_markup=product_detail_kb(product.id))
    await call.answer()


@router.callback_query(F.data.startswith("add:"))
async def add_product_to_cart(call: CallbackQuery, session: AsyncSession) -> None:
    product_id = int(call.data.split(":")[1])
    user = await get_user_by_telegram_id(session, call.from_user.id)
    if not user:
        await call.answer("ابتدا /start را ارسال کنید.", show_alert=True)
        return

    success, message = await add_to_cart(session, user.id, product_id)
    await call.answer(message, show_alert=not success)
