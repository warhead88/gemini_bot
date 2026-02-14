from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from src.services.redis_storage import RedisStorage

class ChatActiveMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if event.text and event.text.startswith(('/start', '/chat')):
                return await handler(event, data)

            user_id = event.from_user.id if event.from_user else 0
            redis: RedisStorage = data.get("redis")
            
            # Проверяем наличие ключа в Redis
            if not redis or not await redis.client.exists(f"chat:{user_id}"):
                await event.answer("Сначала введите команду /chat, чтобы начать общение!")
                return

        return await handler(event, data)