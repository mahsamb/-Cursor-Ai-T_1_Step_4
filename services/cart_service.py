from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import CartItem, Product, User


async def add_to_cart(session: AsyncSession, user_id: int, product_id: int) -> tuple[bool, str]:
    product_query = await session.execute(select(Product).where(Product.id == product_id))
    product = product_query.scalar_one_or_none()
    if not product:
        return False, "محصول پیدا نشد."
    if product.stock <= 0:
        return False, "این محصول فعلا موجود نیست."

    item_query = await session.execute(
        select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
    )
    cart_item = item_query.scalar_one_or_none()

    if cart_item:
        if cart_item.quantity >= product.stock:
            return False, "موجودی کافی برای افزودن بیشتر وجود ندارد."
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
        session.add(cart_item)

    await session.commit()
    return True, "محصول به سبد خرید اضافه شد."


async def get_user_cart(session: AsyncSession, user_id: int) -> list[CartItem]:
    query = await session.execute(
        select(CartItem)
        .options(selectinload(CartItem.product).selectinload(Product.brand))
        .where(CartItem.user_id == user_id)
    )
    return list(query.scalars().all())


async def remove_cart_item(session: AsyncSession, user_id: int, cart_item_id: int) -> bool:
    query = await session.execute(
        select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == user_id)
    )
    item = query.scalar_one_or_none()
    if not item:
        return False
    await session.delete(item)
    await session.commit()
    return True


async def change_cart_item_quantity(
    session: AsyncSession, user_id: int, cart_item_id: int, delta: int
) -> tuple[bool, str]:
    query = await session.execute(
        select(CartItem)
        .options(selectinload(CartItem.product))
        .where(CartItem.id == cart_item_id, CartItem.user_id == user_id)
    )
    item = query.scalar_one_or_none()
    if not item:
        return False, "آیتم سبد یافت نشد."

    new_quantity = item.quantity + delta
    if new_quantity <= 0:
        await session.delete(item)
        await session.commit()
        return True, "آیتم از سبد حذف شد."

    if new_quantity > item.product.stock:
        return False, "تعداد درخواستی بیشتر از موجودی است."

    item.quantity = new_quantity
    await session.commit()
    return True, "تعداد محصول در سبد بروزرسانی شد."


async def clear_cart(session: AsyncSession, user_id: int) -> None:
    items = await get_user_cart(session, user_id)
    for item in items:
        await session.delete(item)
    await session.commit()


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    query = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return query.scalar_one_or_none()
