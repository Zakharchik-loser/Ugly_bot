import logging
from aiogram import Bot, Dispatcher
from config import Bot_token
from handlers.commands import register_commands
from handlers.callbacks import register_callbacks

logging.basicConfig(level=logging.INFO)
bot = Bot(token=Bot_token)
dp = Dispatcher()

async def main():
    register_commands(dp)
    register_callbacks(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
