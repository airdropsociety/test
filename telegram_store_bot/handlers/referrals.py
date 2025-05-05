# handlers/referrals.py
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.referrals_keyboard import get_referrals_keyboard
from database.crud import get_user_referrals

router = Router()

@router.message(Command("referrals"))
@router.callback_query(lambda c: c.data == "referrals")
async def show_referral_info(
    message_or_callback: types.Message | types.CallbackQuery,
    session: AsyncSession  # Database session injected by middleware
):
    try:
        # Get user ID from the incoming message or callback
        user_id = message_or_callback.from_user.id
        
        # Fetch referrals from database
        referrals = await get_user_referrals(session, user_id)
        referral_count = len(referrals)
        balance = sum(ref.commission for ref in referrals) if referrals else 0
        
        text = (
            f"👥 <b>Referral System</b>\n\n"
            f"🔗 <b>Your referral link:</b>\n"
            f"https://t.me/{(await message_or_callback.bot.get_me()).username}?start={user_id}\n\n"
            f"👫 <b>Referrals:</b> {referral_count}\n"
            f"💰 <b>Balance:</b> {balance:.4f} USDT\n"
            f"⭐ <b>Available stars:</b> ~{int(balance / 0.017) if balance else 0}\n\n"
            f"💎 You get 30% commission from each referral purchase!"
        )
        
        reply_markup = get_referrals_keyboard(balance >= 0.017 * 50)  # Only enable if enough for min purchase
        
        if isinstance(message_or_callback, types.Message):
            await message_or_callback.answer(text, reply_markup=reply_markup)
        else:
            await message_or_callback.message.edit_text(text, reply_markup=reply_markup)
            
    except Exception as e:
        error_msg = "❌ Error loading referral information"
        if isinstance(message_or_callback, types.Message):
            await message_or_callback.answer(error_msg)
        else:
            await message_or_callback.message.edit_text(error_msg)
        print(f"Referral error: {e}")