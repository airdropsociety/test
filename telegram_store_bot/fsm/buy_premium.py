# fsm/buy_premium.py
from aiogram.fsm.state import StatesGroup, State

class BuyPremiumStates(StatesGroup):
    choosing_recipient = State()  # Renamed from choosing_premium_recipient
    choosing_period = State()
    confirming_payment = State()