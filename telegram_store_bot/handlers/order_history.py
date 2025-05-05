from aiogram import Router, types
from aiogram.filters import Command
from keyboards.order_history_keyboard import get_order_history_keyboard
from database.crud import get_user_orders

router = Router()

@router.message(Command("history"))
@router.callback_query(lambda c: c.data == "order_history")
async def show_order_history(message_or_callback: types.Message | types.CallbackQuery, user_id: int):
    orders = await get_user_orders(user_id)
    
    if not orders:
        text = "📑 You don't have any orders yet."
    else:
        text = "📑 Order history:\n\n"
        text += "\n".join(
            f"• Order #{order.id} - {order.product} - {order.status}"
            for order in orders[:10]  # Show last 10 orders
        )
    
    reply_markup = get_order_history_keyboard(orders)
    
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.edit_text(text, reply_markup=reply_markup)