from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards.calculator_keyboard import get_calculator_keyboard
from services.price_calculator import calculate_stars_to_currency, calculate_currency_to_stars

router = Router()

@router.message(Command("calculator"))
@router.callback_query(lambda c: c.data == "calculate")
async def show_calculator_options(message_or_callback: types.Message | types.CallbackQuery):
    text = """
🔢 Calculator
Select what you want to calculate:
💳 • Amount in USDT/TON - find out the number of stars for the entered amount
⭐ • Amount in stars - find out the cost of the entered number of stars
    """
    
    reply_markup = get_calculator_keyboard()
    
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.edit_text(text, reply_markup=reply_markup)

@router.callback_query(F.data == "calc_currency_to_stars")
async def request_currency_amount(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CalculatorState.waiting_for_currency)
    await callback.message.edit_text(
        "✍️ Enter the amount in USDT/TON to find out how many stars you can buy\n"
        "📒 For example: 10",
        reply_markup=get_calculator_keyboard(back_only=True)
    )

@router.callback_query(F.data == "calc_stars_to_currency")
async def request_stars_amount(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CalculatorState.waiting_for_stars)
    await callback.message.edit_text(
        "✍️ Enter the number of stars to find out their value\n"
        "📒 For example: 100",
        reply_markup=get_calculator_keyboard(back_only=True)
    )

@router.message(CalculatorState.waiting_for_currency)
async def show_currency_calculation(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        stars = await calculate_currency_to_stars(amount)
        await message.answer(
            f"💵 {amount} USDT ≈ {stars}⭐\n"
            f"💎 {amount} TON ≈ {stars}⭐",
            reply_markup=get_calculator_keyboard(back_only=True)
        )
    except ValueError:
        await message.answer("Please enter a valid number")

@router.message(CalculatorState.waiting_for_stars)
async def show_stars_calculation(message: types.Message, state: FSMContext):
    try:
        stars = int(message.text)
        usdt, ton = await calculate_stars_to_currency(stars)
        await message.answer(
            f"⭐ {stars} stars ≈\n"
            f"💵 {usdt:.4f} USDT\n"
            f"💎 {ton:.4f} TON",
            reply_markup=get_calculator_keyboard(back_only=True)
        )
    except ValueError:
        await message.answer("Please enter a valid integer number of stars")