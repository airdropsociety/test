from typing import Union
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from fsm.buy_stars import BuyStarsStates
from keyboards.buy_stars_keyboard import buy_stars_kb
from keyboards.premium_keyboard import premium_period_kb, premium_payment_kb
from keyboards.main_keyboard import main_menu_kb

router = Router()

def get_username_selection_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Buy for yourself", callback_data="recipient_self")],
        [InlineKeyboardButton(text="↩️ Back", callback_data="buy_stars")]
    ])

async def show_buy_stars_view(update: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()
    
    # Only proceed if we're not currently asking for username
    current_state = await state.get_state()
    if current_state == BuyStarsStates.choosing_username.state:
        return
    """Helper function to display the main Buy Stars view by editing the bot's last message"""
    data = await state.get_data()
    username = data.get("username", "")
    quantity = data.get("quantity", "")
    bot_message_id = data.get("bot_message_id")

    username_display = f"@{username}" if username else ""
    quantity_display = quantity if quantity else ""

    text = (
        "⭐ *Buy Stars*\n"
        f"👤 *Username\\:* {username_display}\n"
        f"✨ *Number of stars\\:* {quantity_display}\n\n"
        "❓ You can buy any number of stars\\. Click 'Enter quantity' and enter any number ≥50\\."
    )

    try:
        if isinstance(update, Message):
            # For new messages from user
            if bot_message_id:
                try:
                    await update.bot.edit_message_text(
                        chat_id=update.chat.id,
                        message_id=bot_message_id,
                        text=text,
                        reply_markup=buy_stars_kb(username, str(quantity)),
                        parse_mode="MarkdownV2"
                    )
                    return
                except:
                    pass  # Fall through to sending new message
            
            msg = await update.answer(
                text=text,
                reply_markup=buy_stars_kb(username, str(quantity)),
                parse_mode="MarkdownV2"
            )
            await state.update_data(bot_message_id=msg.message_id)
            
        else:  # CallbackQuery
            # Always edit the callback's message
            await update.message.edit_text(
                text=text,
                reply_markup=buy_stars_kb(username, str(quantity)),
                parse_mode="MarkdownV2"
            )
            await state.update_data(bot_message_id=update.message.message_id)
            
    except Exception as e:
        print(f"Error in show_buy_stars_view: {e}")
        if isinstance(update, Message):
            msg = await update.answer(
                text=text,
                reply_markup=buy_stars_kb(username, str(quantity)),
                parse_mode="MarkdownV2"
            )
            await state.update_data(bot_message_id=msg.message_id)
        else:
            await update.message.answer(
                text=text,
                reply_markup=buy_stars_kb(username, str(quantity)),
                parse_mode="MarkdownV2"
            )

@router.callback_query(lambda c: c.data == "buy_stars")
async def handle_buy_stars(callback: CallbackQuery, state: FSMContext):
    await state.update_data(bot_message_id=callback.message.message_id)
    await show_buy_stars_view(callback, state)  # Pass callback.message instead of callback

@router.callback_query(lambda c: c.data == "enter_username")
async def ask_username(callback: CallbackQuery, state: FSMContext):
    # Clear any existing quantity to prevent state conflicts
    await state.update_data(quantity="")
    
    await callback.message.edit_text(
        "👤 *Specify the recipient*\n\n"
        "🆔 Enter the @username of the account\\.\n"
        "❗Make sure the account exists\\.\n\n"
        "Or click below to use your own account\\.",
        parse_mode="MarkdownV2",
        reply_markup=get_username_selection_kb()
    )
    await state.set_state(BuyStarsStates.choosing_username)
    await callback.answer()

@router.message(BuyStarsStates.choosing_username)
async def save_username(message: Message, state: FSMContext):
    username = message.text.strip().lstrip("@")
    
    if not username or len(username) < 3:
        await message.answer("❌ Invalid username. Please enter a valid @username.")
        return

    # Update state with new username
    await state.update_data(username=username)
    
    try:
        await message.delete()  # Clean up user's input
    except:
        pass
    
    # Clear the username input state
    await state.set_state(None)
    
    # Show the main view with the new username
    await show_buy_stars_view(message, state)

@router.callback_query(lambda c: c.data == "recipient_self")
async def set_self_as_recipient(callback: CallbackQuery, state: FSMContext):
    username = callback.from_user.username
    if not username:
        await callback.answer("❌ You don't have a username set.", show_alert=True)
        return

    # Clear any existing state and set username
    await state.update_data(username=username, quantity="")
    await state.set_state(None)  # Clear any active state
    
    await show_buy_stars_view(callback, state)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("quantity_"))
async def set_fixed_quantity(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    # If no username exists, prompt for it
    if not data.get("username"):
        await callback.answer("❌ Please set a recipient first.", show_alert=True)
        await ask_username(callback, state)
        return
    
    quantity = callback.data.split("_")[1]
    
    # Update state and show view
    await state.update_data(quantity=quantity)
    await show_buy_stars_view(callback, state)
    await callback.answer()

@router.callback_query(lambda c: c.data == "enter_quantity")
async def ask_custom_quantity(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyStarsStates.choosing_quantity)
    data = await state.get_data()
    bot_message_id = data.get("bot_message_id")
    
    try:
        await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=bot_message_id,
            text="✍️ *Enter quantity*\n\n"
                 "⭐ You can buy any number of stars \\(minimum 50\\), just enter the number\\:",
            parse_mode="MarkdownV2"
        )
    except:
        await callback.message.answer(
            "✍️ *Enter quantity*\n\n"
            "⭐ You can buy any number of stars \\(minimum 50\\), just enter the number\\:",
            parse_mode="MarkdownV2"
        )
    await callback.answer()

@router.message(BuyStarsStates.choosing_quantity)
async def save_custom_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)
        if quantity < 50:
            await message.answer("❌ Minimum quantity is 50 stars.")
            return
            
        await state.update_data(quantity=str(quantity))
        await message.delete()
        
        data = await state.get_data()
        if not data.get("username"):
            await ask_username(message, state)
            return
            
        await show_buy_stars_view(message, state)
        
    except ValueError:
        await message.answer("❌ Please enter a valid number.")


@router.callback_query(lambda c: c.data == "continue")
async def proceed_to_payment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("username") or not data.get("quantity"):
        await callback.answer("❌ Please select both username and quantity first.", show_alert=True)
        return
    
    text = (
        "💳 *Select payment method*\n\n"
        f"👤 *User\\:* @{data['username']}\n"
        f"⭐ *Quantity\\:* {data['quantity']}\n\n"
        "Choose your payment method\\:"
    )
    
    payment_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💲 USDT", callback_data="payment_usdt"),
         InlineKeyboardButton(text="💎 TON", callback_data="payment_ton")],
        [InlineKeyboardButton(text="↩️ Back", callback_data="buy_stars")]
    ])
    
    await callback.message.edit_text(
        text=text,
        reply_markup=payment_kb,
        parse_mode="MarkdownV2"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("payment_"))
async def show_payment_details(callback: CallbackQuery, state: FSMContext):
    payment_method = callback.data.split("_")[1]
    data = await state.get_data()
    
    # Calculate amount based on quantity and payment method
    stars = int(data['quantity'])
    rate = 0.017 if payment_method == "usdt" else 0.017 * 2.5  # Example rate for TON
    amount = stars * rate
    
    text = (
        "⏳ *The order is valid for 30 minutes*\n\n"
        f"💰 *Amount\\:* {amount:.4f} {'USDT' if payment_method == 'usdt' else 'TON'}\n"
        f"🆔 *Order number\\:* {callback.message.message_id}\n\n"
        "🛟 If you have any problems, please contact support\\."
    )
    
    payment_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Pay", callback_data=f"process_payment_{payment_method}")],
        [InlineKeyboardButton(text="↩️ Back", callback_data="continue")]
    ])
    
    await callback.message.edit_text(
        text=text,
        reply_markup=payment_kb,
        parse_mode="MarkdownV2"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    from handlers.main_menu import main_menu_kb
    
    await state.clear()
    
    name = callback.from_user.first_name.replace("_", "\\_").replace("*", "\\*").replace(".", "\\.").replace("!", "\\!")
    
    text = (
        f"👋 Hello, *{name}*\\!\n\n"
        f"⭐ Here you can buy Telegram stars without KYC and cheaper than the app\\."
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=main_menu_kb(),
        parse_mode="MarkdownV2"
    )
    await callback.answer()

def escape_markdown(text: str) -> str:
    """Escape all special MarkdownV2 characters while preserving intentional formatting"""
    escape_chars = '_*[]()~`>#+-=|{}.!'
    text = ''.join(f'\\{char}' if char in escape_chars else char for char in text)
    return text.replace('\\*', '*').replace('\\_', '_')

async def show_premium_view(update: Union[Message, CallbackQuery], state: FSMContext):
    """Main premium subscription view"""
    data = await state.get_data()
    username = data.get("premium_username", "")
    months = data.get("premium_months", "")

    text = escape_markdown(
        "🎁 *Buy Premium*\n"
        f"👤 *Username:* @{username}\n" if username else "👤 *Username:* \n"
        f"⏳ *Period:* {months} Months\n\n" if months else "⏳ *Period:* \n\n"
        "Please choose the period (3, 6, or 12 months)"
    )

    try:
        if isinstance(update, Message):
            msg = await update.answer(
                text=text,
                reply_markup=premium_period_kb(username, months),
                parse_mode="MarkdownV2"
            )
            await state.update_data(bot_message_id=msg.message_id)
        else:
            await update.message.edit_text(
                text=text,
                reply_markup=premium_period_kb(username, months),
                parse_mode="MarkdownV2"
            )
    except Exception as e:
        print(f"Error showing premium view: {e}")
        msg = await update.answer(
            text=text,
            reply_markup=premium_period_kb(username, months),
            parse_mode="MarkdownV2"
        )
        if hasattr(msg, 'message_id'):
            await state.update_data(bot_message_id=msg.message_id)

@router.callback_query(lambda c: c.data == "buy_premium")
async def handle_buy_premium(callback: CallbackQuery, state: FSMContext):
    """Entry point for premium purchase"""
    await state.update_data(
        premium_username="",
        premium_months="",
        bot_message_id=callback.message.message_id
    )
    await show_premium_view(callback, state)
    await callback.answer()

@router.callback_query(lambda c: c.data == "premium_recipient")
async def ask_premium_username(callback: CallbackQuery, state: FSMContext):
    """Username prompt with perfect MarkdownV2 escaping"""
    await callback.message.edit_text(
        text=escape_markdown(
            "👤 *Specify the recipient*\n\n"
            "🆔 Enter the @username of the account\n"
            "❗Make sure the account exists\n\n"
            "Or click below to use your own account."
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Buy for myself", callback_data="premium_self")],
            [InlineKeyboardButton(text="↩️ Back", callback_data="buy_premium")]
        ]),
        parse_mode="MarkdownV2"
    )
    await state.set_state(BuyStarsStates.choosing_premium_recipient)
    await callback.answer()

@router.callback_query(lambda c: c.data == "premium_self")
async def set_premium_self(callback: CallbackQuery, state: FSMContext):
    """Set recipient to user's own username"""
    if not callback.from_user.username:
        await callback.answer("❌ You don't have a username set", show_alert=True)
        return

    await state.update_data(premium_username=callback.from_user.username)
    await state.set_state(None)
    await show_premium_view(callback, state)
    await callback.answer()

@router.message(BuyStarsStates.choosing_premium_recipient)
async def save_premium_username(message: Message, state: FSMContext):
    """Save manually entered username"""
    username = message.text.strip().lstrip("@")
    if not username or len(username) < 3:
        await message.answer("❌ Invalid username. Please enter a valid @username.")
        return

    await state.update_data(premium_username=username)
    try:
        await message.delete()
    except:
        pass
    
    await state.set_state(None)
    await show_premium_view(message, state)

@router.callback_query(lambda c: c.data.startswith("premium_period_"))
async def set_premium_period(callback: CallbackQuery, state: FSMContext):
    """Set selected premium period"""
    months = callback.data.split("_")[2]
    await state.update_data(premium_months=months)
    await show_premium_view(callback, state)
    await callback.answer()

@router.callback_query(lambda c: c.data == "premium_continue")
async def premium_continue(callback: CallbackQuery, state: FSMContext):
    """Proceed to payment selection"""
    data = await state.get_data()
    if not data.get("premium_username"):
        await callback.answer("❌ Please set a recipient first", show_alert=True)
        return
    if not data.get("premium_months"):
        await callback.answer("❌ Please select a period first", show_alert=True)
        return

    await callback.message.edit_text(
        text=escape_markdown(
            f"💳 *Confirm Premium*\n\n"
            f"👤 *Recipient\\:* @{data['premium_username']}\n"
            f"⏳ *Period\\:* {data['premium_months']} Months\n\n"
            "Select payment method\\:"
        ),
        reply_markup=premium_payment_kb(),
        parse_mode="MarkdownV2"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("premium_pay_"))
async def show_premium_invoice(callback: CallbackQuery, state: FSMContext):
    """Show payment invoice"""
    payment_method = callback.data.split("_")[2]
    data = await state.get_data()
    
    # Calculate amount based on period
    prices = {3: 13.5, 6: 18.5, 12: 33}
    amount = prices.get(int(data['premium_months']), 0)
    
    await callback.message.edit_text(
        text=escape_markdown(
            "⏳ *Invoice*\n\n"
            f"💰 *Amount\\:* {amount} {'USDT' if payment_method == 'usdt' else 'TON'}\n"
            f"⏳ *Valid for\\:* 30 minutes\n\n"
            f"🆔 *Order\\:* {callback.message.message_id}\n\n"
            "❗ Payment instructions will appear here"
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Pay Now", callback_data=f"process_premium_{payment_method}")],
            [InlineKeyboardButton(text="↩️ Back", callback_data="premium_continue")]
        ]),
        parse_mode="MarkdownV2"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Handle back to main menu from premium flow"""
    await state.clear()
    
    name = callback.from_user.first_name
    text = escape_markdown(
        f"👋 Hello, *{name}*!\n\n"
        f"⭐ Here you can buy Telegram stars without KYC and cheaper than the app."
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=main_menu_kb(),
        parse_mode="MarkdownV2"
    )
    await callback.answer()