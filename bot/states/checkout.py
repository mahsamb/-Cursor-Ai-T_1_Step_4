from aiogram.fsm.state import State, StatesGroup


class CheckoutStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()
