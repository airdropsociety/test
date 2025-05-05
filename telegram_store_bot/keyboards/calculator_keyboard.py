# keyboards/calculator_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_calculator_keyboard(back_only=False):
    if back_only:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="↩️ Back", callback_data="calculate")]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Amount in dollars", callback_data="calc_currency_to_stars"),
                InlineKeyboardButton(text="⭐ Amount in stars", callback_data="calc_stars_to_currency")
            ],
            [InlineKeyboardButton(text="↩️ Back", callback_data="back_to_main")]
        ]
    )