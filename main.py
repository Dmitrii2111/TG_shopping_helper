import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import config
from bot.database.db import init_db
from bot.handlers.base import base_router

from bot.handlers.base import base_router
from bot.handlers.shopping import shopping_router 
from bot.handlers.voice import voice_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting bot...")

    # 1. Initialize the Database
    await init_db()

    # 2. Initialize Bot and Dispatcher
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # 3. Include Routers
    dp.include_router(base_router)
    dp.include_router(shopping_router)
    dp.include_router(voice_router)

    # 4. Start polling
    try:
        # Drop pending updates to avoid spamming the bot on startup
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Graceful shutdown
        await bot.session.close()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Application interrupted by user.")