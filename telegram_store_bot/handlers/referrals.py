from aiogram import Router, types
from aiogram.filters import Command
from keyboards.referrals_keyboard import get_referrals_keyboard
from database.crud import get_user_referrals

router = Router()

@router.message(Command("referrals"))
@router.callback_query(lambda c: c.data == "referrals")
async def show_referral_info(message_or_callback: types.Message | types.CallbackQuery, user_id: int):
    referrals = await get_user_referrals(user_id)
    referral_count = len(referrals)
    balance = sum(ref.commission for ref in referrals)
    
    text = f"""
👥 Referral system

🔗 Your referral link:
https://t.me/monostarsbot?start={user_id}

👫 Number of referrals: {referral_count}
💰 Balance: {balance:.4f} USDT
⭐ Available for purchase: ~{int(balance / 0.017)} stars

💎 You get 30% of our earnings from each purchase of your referral.
    """
    
    reply_markup = get_referrals_keyboard(balance >= 0.017 * 50)  # Only enable if enough for min purchase
    
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.edit_text(text, reply_markup=reply_markup)