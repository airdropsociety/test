from aiogram.fsm.state import StatesGroup, State

class BuyStarsStates(StatesGroup):
    choosing_username = State()
    choosing_quantity = State()
    confirming_payment = State()
    last_bot_message = State()  # Track the last bot message ID
    choosing_premium_period = State()
    choosing_premium_recipient = State()
    confirming_premium_payment = State()