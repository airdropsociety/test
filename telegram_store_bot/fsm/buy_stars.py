# fsm/buy_stars.py
from aiogram.fsm.state import StatesGroup, State

class BuyStarsStates(StatesGroup):
    choosing_username = State()
    choosing_quantity = State()
    confirming_payment = State()