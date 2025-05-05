import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import main_menu  # Import the file, not a function
from handlers import buy_stars
load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(main_menu.router)  # Include the router here
    dp.include_router(buy_stars.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
