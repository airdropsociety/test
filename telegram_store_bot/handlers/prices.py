# Standard imports for most handlers
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import Router, types
from aiogram.filters import Command
from keyboards.prices_keyboard import get_prices_keyboard

router = Router()

@router.message(Command("prices"))
@router.callback_query(lambda c: c.data == "prices")
async def show_prices(message_or_callback: types.Message | types.CallbackQuery):
    text = """
💱 Star rate
1⭐ = 0.017 USDT
1⭐ = {} TON

💱 Premium prices
🎁3 Months = 13.5$
🎁6 Months = 18.5$
🎁12 Months = 33$
    """
    
    reply_markup = get_prices_keyboard()
    
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.edit_text(text, reply_markup=reply_markup)