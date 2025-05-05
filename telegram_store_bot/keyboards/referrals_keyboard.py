# keyboards/referrals_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_referrals_keyboard(has_balance):
    buttons = []
    if has_balance:
        buttons.append([InlineKeyboardButton(
            text="⭐ Buy stars with your commission",
            callback_data="buy_with_commission"
        )])
    buttons.append([InlineKeyboardButton(text="↩️ Back", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)