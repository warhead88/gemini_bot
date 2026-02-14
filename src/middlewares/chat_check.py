from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from src.services.gemini import is_chat_active

class ChatActiveMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Проверяем только сообщения (Message)
        if isinstance(event, Message):
            # Игнорируем команды /start и /chat (чтобы их можно было вызвать всегда)
            if event.text and event.text.startswith(('/start', '/chat')):
                return await handler(event, data)

            user_id = event.from_user.id if event.from_user else 0
            
            # Если чат не активен — прерываем цепочку и отвечаем пользователю
            if not is_chat_active(user_id):
                await event.answer("Сначала введите команду /chat, чтобы начать общение!")
                return # Хендлер даже не будет вызван!

        # Если всё ок — идем дальше к хендлеру
        return await handler(event, data)