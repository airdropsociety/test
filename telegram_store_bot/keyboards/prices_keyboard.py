# keyboards/prices_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_prices_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Back", callback_data="back_to_main")]
        ]
    )