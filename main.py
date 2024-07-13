import asyncio
import logging
from aiogram import types, Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
import sys
from dotenv import load_dotenv
from bot.handlers.user_handlers import user_router
from bot.handlers.admin_handlers import admin_router
from bot.keyboards.user_keyboards import setup_bot_commands
from bot.middleware.Middleware import AlbumMiddleware
import os


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
GREEN = "\033[92m"
RESET = "\033[0m"
print(f'{GREEN}Бот запущен{RESET}')


async def main() -> None:
    """Entry point
    """
    load_dotenv('.env')
    TOKEN = os.getenv('TOKEN')
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await setup_bot_commands(bot)
    dp.message.middleware(AlbumMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())