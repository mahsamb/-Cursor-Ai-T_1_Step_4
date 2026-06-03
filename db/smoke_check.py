import asyncio

from sqlalchemy import func, select

from db.models import Base, Brand, Category, Order, Product
from db.seed import seed_data, seed_sample_order
from db.session import AsyncSessionLocal, engine


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_data(session)
        sample_created = await seed_sample_order(session)
        categories = (await session.execute(select(func.count(Category.id)))).scalar_one()
        brands = (await session.execute(select(func.count(Brand.id)))).scalar_one()
        products = (await session.execute(select(func.count(Product.id)))).scalar_one()
        orders = (await session.execute(select(func.count(Order.id)))).scalar_one()
        print(
            f"smoke_ok categories={categories} brands={brands} "
            f"products={products} orders={orders} "
            f"sample_order={'yes' if sample_created else 'skipped'}"
        )


if __name__ == "__main__":
    asyncio.run(main())
