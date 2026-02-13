"""Сервис для диалога с моделью Gemini (Google GenAI SDK)."""

import logging
from typing import Any

from google import genai

from src.config import get_gemini_api_key

logger = logging.getLogger(__name__)

# Модель по умолчанию
GEMINI_MODEL = "gemini-2.5-flash"

# Активные чат-сессии: user_id -> async chat
_active_chats: dict[int, Any] = {}


def _get_client() -> genai.Client:
    """Возвращает клиент GenAI (читает GEMINI_API_KEY из окружения)."""
    return genai.Client(api_key=get_gemini_api_key())


def start_chat(user_id: int) -> None:
    """Запускает диалог с ИИ для пользователя. Создаёт новую сессию чата."""
    if user_id in _active_chats:
        return
    client = _get_client()
    # create() возвращает AsyncChat, а не корутину — await не нужен
    chat = client.aio.chats.create(model=GEMINI_MODEL)
    _active_chats[user_id] = chat
    logger.info("Чат запущен для user_id=%s", user_id)


def stop_chat(user_id: int) -> bool:
    """Завершает диалог для пользователя. Возвращает True, если сессия была активна."""
    if user_id in _active_chats:
        del _active_chats[user_id]
        logger.info("Чат остановлен для user_id=%s", user_id)
        return True
    return False


def is_chat_active(user_id: int) -> bool:
    """Проверяет, активен ли диалог с ИИ для пользователя."""
    return user_id in _active_chats


async def send_message(user_id: int, text: str) -> str:
    """
    Отправляет сообщение в диалог Gemini и возвращает ответ модели.
    Вызывать только при активном чате (is_chat_active(user_id) == True).
    """
    chat = _active_chats.get(user_id)
    if not chat:
        return "Диалог не активен. Используйте /chat чтобы начать."
    try:
        response = await chat.send_message(text)
        return response.text or ""
    except Exception as e:
        logger.exception("Ошибка Gemini для user_id=%s: %s", user_id, e)
        return f"Ошибка при обращении к ИИ: {e!s}"