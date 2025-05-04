from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def buy_stars_kb(username: str = "", quantity: str = "") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"50⭐{' ✅' if quantity == '50' else ''}", 
                callback_data="quantity_50"
            ),
            InlineKeyboardButton(
                text=f"100⭐{' ✅' if quantity == '100' else ''}", 
                callback_data="quantity_100"
            ),
            InlineKeyboardButton(
                text=f"500⭐{' ✅' if quantity == '500' else ''}", 
                callback_data="quantity_500"
            ),
            InlineKeyboardButton(
                text=f"1000⭐{' ✅' if quantity == '1000' else ''}", 
                callback_data="quantity_1000"
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"👤 The recipient: @{username}" if username else "👤 The recipient",
                callback_data="enter_username"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🌟 Enter quantity{' ✅' if quantity and not quantity.isdigit() else ''}",
                callback_data="enter_quantity"
            )
        ]
    ]
    
    if username and quantity:
        buttons.append([
            InlineKeyboardButton(text="↩️ Back", callback_data="back_to_main"),  # Changed this
            InlineKeyboardButton(text="➡️ Continue", callback_data="continue")
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="↩️ Back", callback_data="back_to_main")  # Changed this
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)