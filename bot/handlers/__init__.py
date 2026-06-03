from aiogram import Dispatcher

from .admin import router as admin_router
from .cart import router as cart_router
from .catalog import router as catalog_router
from .checkout import router as checkout_router
from .orders import router as orders_router
from .search import router as search_router
from .start import router as start_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(catalog_router)
    dp.include_router(search_router)
    dp.include_router(cart_router)
    dp.include_router(checkout_router)
    dp.include_router(orders_router)
from aiogram import Dispatcher

from .cart import router as cart_router
from .catalog import router as catalog_router
from .checkout import router as checkout_router
from .orders import router as orders_router
from .search import router as search_router
from .start import router as start_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(search_router)
    dp.include_router(cart_router)
    dp.include_router(checkout_router)
    dp.include_router(orders_router)
