from aiogram.fsm.state import StatesGroup, State

class CalculatorState(StatesGroup):
    waiting_for_currency = State()
    waiting_for_stars = State()