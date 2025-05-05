# bot.py
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

# Handler imports
from handlers.main_menu import router as main_router
from handlers.buy_stars import router as buy_stars_router
from handlers.buy_premium import router as buy_premium_router
from handlers.prices import router as prices_router
from handlers.order_history import router as order_history_router
from handlers.referrals import router as referrals_router
from handlers.calculator import router as calculator_router

load_dotenv()

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker
    
    async def __call__(self, handler, event, data):
        async with self.sessionmaker() as session:
            data["session"] = session  # Changed key from "db" to "session"
            return await handler(event, data)

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())

    # Setup database connection
    engine = create_async_engine("sqlite+aiosqlite:///database.db")
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    # Add database middleware
    dp.update.middleware(DbSessionMiddleware(sessionmaker))
    
    # Include routers
    dp.include_router(main_router)
    dp.include_router(buy_stars_router)
    dp.include_router(buy_premium_router)
    dp.include_router(prices_router)
    dp.include_router(order_history_router)
    dp.include_router(referrals_router)
    dp.include_router(calculator_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())