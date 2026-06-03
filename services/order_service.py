from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import CartItem, Order, OrderItem, Product


async def create_order_from_cart(
    session: AsyncSession, user_id: int, phone: str, address: str
) -> Order | None:
    cart_query = await session.execute(
        select(CartItem)
        .options(selectinload(CartItem.product))
        .where(CartItem.user_id == user_id)
    )
    cart_items = list(cart_query.scalars().all())
    if not cart_items:
        return None

    total_price = sum(item.quantity * item.product.price for item in cart_items)
    order = Order(user_id=user_id, total_price=total_price, phone=phone, address=address)
    session.add(order)
    await session.flush()

    for item in cart_items:
        session.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price,
            )
        )
        item.product.stock = max(0, item.product.stock - item.quantity)
        await session.delete(item)

    await session.commit()
    await session.refresh(order)
    return order


async def get_user_orders(session: AsyncSession, user_id: int) -> list[Order]:
    query = await session.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .where(Order.user_id == user_id)
        .order_by(Order.id.desc())
    )
    return list(query.scalars().all())
