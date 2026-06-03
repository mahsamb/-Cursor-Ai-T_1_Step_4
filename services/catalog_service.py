from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Category, Product


async def get_categories(session: AsyncSession) -> list[Category]:
    result = await session.execute(select(Category).order_by(Category.name))
    return list(result.scalars().all())


async def get_products_by_category(session: AsyncSession, category_id: int) -> list[Product]:
    result = await session.execute(
        select(Product)
        .options(selectinload(Product.brand))
        .where(Product.category_id == category_id)
        .order_by(Product.name)
    )
    return list(result.scalars().all())


async def get_products_by_category_paged(
    session: AsyncSession, category_id: int, page: int, page_size: int = 5
) -> tuple[list[Product], int]:
    products = await get_products_by_category(session, category_id)
    total = len(products)
    start = max(page, 0) * page_size
    end = start + page_size
    return products[start:end], total


async def get_category_by_id(session: AsyncSession, category_id: int) -> Category | None:
    result = await session.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    result = await session.execute(
        select(Product).options(selectinload(Product.brand)).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def search_products(session: AsyncSession, term: str) -> list[Product]:
    result = await session.execute(
        select(Product)
        .options(selectinload(Product.brand))
        .where(Product.name.ilike(f"%{term}%"))
        .order_by(Product.name)
    )
    return list(result.scalars().all())
