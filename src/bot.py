"""Точка входа: запуск бота."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.config import get_bot_token
from src.handlers import main_router
from src.middlewares.chat_check import ChatActiveMiddleware
from src.services.redis_storage import RedisStorage

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Инициализация бота
    bot = Bot(
        token=get_bot_token(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    
    # Инициализация Redis (Единая точка входа для БД)
    redis_storage = RedisStorage()
    
    dp = Dispatcher()
    
    # Пробрасываем redis_storage во все хендлеры и middleware
    dp["redis"] = redis_storage
    
    dp.include_router(main_router)
    dp.message.middleware(ChatActiveMiddleware())
    
    logger.info("Бот запускается с поддержкой Redis...")
    
    try:
        await dp.start_polling(bot)
    finally:
        # Закрываем соединение с Redis при выключении
        await redis_storage.client.aclose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
