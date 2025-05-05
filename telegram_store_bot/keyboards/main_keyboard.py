from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# keyboards/main_keyboard.py - FIXED
def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Buy Stars", callback_data="buy_stars")],
            [InlineKeyboardButton(text="🎁 Buy Premium", callback_data="buy_premium")],
            [
                InlineKeyboardButton(text="💰 The Prices", callback_data="prices"),
                InlineKeyboardButton(text="📑 Order History", callback_data="order_history")  # Changed from "history"
            ],
            [
                InlineKeyboardButton(text="👥 Referrals", callback_data="referrals"),
                InlineKeyboardButton(text="🧮 Calculate", callback_data="calculate")
            ],
        ]
    )
