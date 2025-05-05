# keyboards/order_history_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_order_history_keyboard(orders):
    buttons = []
    for order in orders:
        buttons.append([InlineKeyboardButton(
            text=f"Order #{order.id} - {order.product}",
            callback_data=f"order_detail_{order.id}"
        )])
    buttons.append([InlineKeyboardButton(text="↩️ Back", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)