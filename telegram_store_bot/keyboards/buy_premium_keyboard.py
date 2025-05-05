from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def premium_period_kb(username: str = "", months: str = "") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"3M{' ✅' if months == '3' else ''}", callback_data="premium_period_3"),
            InlineKeyboardButton(text=f"6M{' ✅' if months == '6' else ''}", callback_data="premium_period_6"),
            InlineKeyboardButton(text=f"12M{' ✅' if months == '12' else ''}", callback_data="premium_period_12")
        ],
        [InlineKeyboardButton(
            text=f"👤 Recipient: @{username}" if username else "👤 Select Recipient", 
            callback_data="premium_recipient"
        )],
        [
            InlineKeyboardButton(text="↩️ Back", callback_data="main_menu"),  # Changed to main_menu
            InlineKeyboardButton(text="➡️ Continue", callback_data="premium_continue")
        ]
    ])

def premium_payment_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💲 Pay with USDT", callback_data="premium_pay_usdt"),
         InlineKeyboardButton(text="💎 Pay with TON", callback_data="premium_pay_ton")],
        [InlineKeyboardButton(text="↩️ Back", callback_data="buy_premium")]
    ])