# Standard imports for most handlers
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_keyboard import main_menu_kb

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    # Escape characters for MarkdownV2
    name = message.from_user.first_name.replace("_", "\\_").replace("*", "\\*").replace(".", "\\.").replace("!", "\\!")

    text = (
        f"👋 Hello, *{name}*\\!\n\n"
        f"⭐ Here you can buy Telegram stars without KYC and cheaper than the app\\."
    )

    await message.answer(text, reply_markup=main_menu_kb(), parse_mode="MarkdownV2")
