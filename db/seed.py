from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Brand, Category, Order, OrderItem, Product, User


async def _get_map(session: AsyncSession, model) -> dict[str, int]:
    result = await session.execute(select(model))
    return {obj.name: obj.id for obj in result.scalars().all()}


async def _add_missing_products(
    session: AsyncSession, cat_map: dict[str, int], brand_map: dict[str, int], products_data: list[dict]
) -> int:
    existing_query = await session.execute(select(Product.name))
    existing_names = set(existing_query.scalars().all())

    to_add = []
    for item in products_data:
        if item["name"] in existing_names:
            continue
        to_add.append(
            Product(
                name=item["name"],
                brand_id=brand_map[item["brand"]],
                category_id=cat_map[item["category"]],
                price=item["price"],
                stock=item["stock"],
                description=item["description"],
            )
        )

    if to_add:
        session.add_all(to_add)
        await session.commit()
    return len(to_add)


async def seed_data(session: AsyncSession) -> None:
    categories = ["Creatine", "Whey", "Gainer", "BCAA", "Vitamin", "Pre-Workout"]
    brands = [
        "Optimum Nutrition",
        "MuscleTech",
        "Dymatize",
        "Universal",
        "Applied Nutrition",
    ]

    existing_categories = await _get_map(session, Category)
    existing_brands = await _get_map(session, Brand)

    for name in categories:
        if name not in existing_categories:
            session.add(Category(name=name))
    for name in brands:
        if name not in existing_brands:
            session.add(Brand(name=name))
    await session.commit()

    cat_map = await _get_map(session, Category)
    brand_map = await _get_map(session, Brand)

    products_data = [
        {"name": "Platinum Creatine", "brand": "MuscleTech", "category": "Creatine", "price": 1250000, "stock": 20, "description": "کراتین خالص با جذب بالا برای افزایش قدرت."},
        {"name": "Micronized Creatine Powder", "brand": "Optimum Nutrition", "category": "Creatine", "price": 1180000, "stock": 15, "description": "کراتین میکرونایز برای عملکرد بهتر در تمرین."},
        {"name": "Creatine Monohydrate 300g", "brand": "Applied Nutrition", "category": "Creatine", "price": 980000, "stock": 18, "description": "افزایش توان و ریکاوری عضلات."},
        {"name": "Whey Gold Standard", "brand": "Optimum Nutrition", "category": "Whey", "price": 3650000, "stock": 10, "description": "پروتئین وی ایزوله و کنسانتره با کیفیت بالا."},
        {"name": "Elite 100% Whey", "brand": "Dymatize", "category": "Whey", "price": 3450000, "stock": 12, "description": "پروتئین سریع‌الجذب مناسب بعد تمرین."},
        {"name": "Mass Tech Extreme 2000", "brand": "MuscleTech", "category": "Gainer", "price": 4200000, "stock": 8, "description": "گینر پرکالری برای افزایش وزن و حجم عضله."},
        {"name": "Real Gains", "brand": "Universal", "category": "Gainer", "price": 2750000, "stock": 11, "description": "گینر با کربوهیدرات پیچیده و پروتئین کافی."},
        {"name": "BCAA 5000 Powder", "brand": "Optimum Nutrition", "category": "BCAA", "price": 1550000, "stock": 14, "description": "آمینو اسید شاخه‌دار برای ریکاوری سریع‌تر."},
        {"name": "Amino X", "brand": "Dymatize", "category": "BCAA", "price": 1680000, "stock": 9, "description": "ترکیب BCAA و الکترولیت برای تمرینات شدید."},
        {"name": "Daily Multivitamin", "brand": "Universal", "category": "Vitamin", "price": 740000, "stock": 25, "description": "مولتی‌ویتامین کامل برای مصرف روزانه ورزشکاران."},
        {"name": "Vitamin D3 5000 IU", "brand": "Applied Nutrition", "category": "Vitamin", "price": 620000, "stock": 22, "description": "کمک به سلامت استخوان و سیستم ایمنی."},
        {"name": "Pre Gold", "brand": "Applied Nutrition", "category": "Pre-Workout", "price": 1980000, "stock": 13, "description": "انرژی و تمرکز بالا پیش از تمرین."},
        {"name": "Creatine HCL Pro", "brand": "Universal", "category": "Creatine", "price": 1430000, "stock": 16, "description": "فرمول HCL برای جذب سریع‌تر و نفخ کمتر."},
        {"name": "Whey Isolate Zero Carb", "brand": "Applied Nutrition", "category": "Whey", "price": 3890000, "stock": 7, "description": "پروتئین ایزوله با کربوهیدرات نزدیک به صفر."},
        {"name": "Nitro Pre-Workout", "brand": "MuscleTech", "category": "Pre-Workout", "price": 2240000, "stock": 9, "description": "افزایش تمرکز، انرژی و پمپ عضلانی."},
        {"name": "Mega Mass Gainer", "brand": "Dymatize", "category": "Gainer", "price": 3990000, "stock": 6, "description": "گینر حرفه‌ای برای دوره افزایش حجم."},
    ]

    await _add_missing_products(session, cat_map, brand_map, products_data)


async def seed_sample_order(session: AsyncSession) -> bool:
    """یک سفارش نمونه برای تست پنل ادمین (فقط اگر سفارشی وجود نداشته باشد)."""
    order_exists = await session.execute(select(Order.id).limit(1))
    if order_exists.first():
        return False

    user_query = await session.execute(select(User).where(User.telegram_id == 999999999))
    user = user_query.scalar_one_or_none()
    if not user:
        user = User(telegram_id=999999999, full_name="کاربر تست")
        session.add(user)
        await session.flush()

    products_query = await session.execute(select(Product).limit(2))
    products = list(products_query.scalars().all())
    if len(products) < 1:
        return False

    total = sum(p.price for p in products)
    order = Order(
        user_id=user.id,
        total_price=total,
        phone="09120000000",
        address="تهران، خیابان نمونه، پلاک ۱۲",
        status="pending_payment",
    )
    session.add(order)
    await session.flush()

    for p in products:
        session.add(
            OrderItem(
                order_id=order.id,
                product_id=p.id,
                quantity=1,
                price=p.price,
            )
        )

    await session.commit()
    return True
