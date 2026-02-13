"""Точка входа: запуск бота."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.config import get_bot_token
from src.handlers import main_router

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(
        token=get_bot_token(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    
    dp = Dispatcher()
    dp.include_router(main_router)
    
    logger.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
