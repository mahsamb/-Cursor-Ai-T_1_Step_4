from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Order, OrderItem, Product


async def get_products_paged(
    session: AsyncSession, page: int, page_size: int = 6
) -> tuple[list[Product], int]:
    query = await session.execute(
        select(Product).options(selectinload(Product.brand)).order_by(Product.name)
    )
    products = list(query.scalars().all())
    total = len(products)
    start = max(page, 0) * page_size
    end = start + page_size
    return products[start:end], total


async def change_product_stock(session: AsyncSession, product_id: int, delta: int) -> tuple[bool, str]:
    query = await session.execute(select(Product).where(Product.id == product_id))
    product = query.scalar_one_or_none()
    if not product:
        return False, "محصول یافت نشد."

    next_stock = product.stock + delta
    if next_stock < 0:
        return False, "موجودی نمی‌تواند منفی شود."

    product.stock = next_stock
    await session.commit()
    return True, "موجودی محصول بروزرسانی شد."


async def get_orders_paged(
    session: AsyncSession, page: int, page_size: int = 6
) -> tuple[list[Order], int]:
    query = await session.execute(select(Order).order_by(Order.id.desc()))
    orders = list(query.scalars().all())
    total = len(orders)
    start = max(page, 0) * page_size
    end = start + page_size
    return orders[start:end], total


async def update_order_status(
    session: AsyncSession, order_id: int, new_status: str
) -> tuple[bool, str]:
    query = await session.execute(select(Order).where(Order.id == order_id))
    order = query.scalar_one_or_none()
    if not order:
        return False, "سفارش یافت نشد."

    order.status = new_status
    await session.commit()
    return True, "وضعیت سفارش بروزرسانی شد."


async def get_order_with_details(session: AsyncSession, order_id: int) -> Order | None:
    query = await session.execute(
        select(Order)
        .options(
            selectinload(Order.user),
            selectinload(Order.items).selectinload(OrderItem.product),
        )
        .where(Order.id == order_id)
    )
    return query.scalar_one_or_none()
