"""Сервис для диалога с моделью Gemini (Google GenAI SDK)."""

import logging
from typing import Any
from google import genai
from src.core.config import get_gemini_api_key

logger = logging.getLogger(__name__)

# Модель по умолчанию
GEMINI_MODEL = "gemini-2.5-flash"

# Активные чат-сессии: user_id -> async chat
_active_chats: dict[int, Any] = {}


def _get_client() -> genai.Client:
    """Возвращает клиент GenAI."""
    return genai.Client(api_key=get_gemini_api_key())


def start_chat(user_id: int) -> None:
    """Запускает новую сессию чата."""
    if user_id in _active_chats:
        return
    client = _get_client()
    chat = client.aio.chats.create(model=GEMINI_MODEL)
    _active_chats[user_id] = chat
    logger.info("Чат запущен для user_id=%s", user_id)


def stop_chat(user_id: int) -> bool:
    """Завершает диалог. Возвращает True, если сессия была активна."""
    if user_id in _active_chats:
        del _active_chats[user_id]
        logger.info("Чат остановлен для user_id=%s", user_id)
        return True
    return False


def is_chat_active(user_id: int) -> bool:
    """Проверяет активность чата."""
    return user_id in _active_chats


async def send_message(user_id: int, text: str) -> str:
    """Отправляет сообщение и возвращает ответ в формате HTML на русском."""
    chat = _active_chats.get(user_id)
    if not chat:
        return "Диалог не активен. Используйте /chat чтобы начать."
    
    prompt = text + "\n\nОтвечай на русском языке в формате HTML (только базовые теги: b, i, u, s, code, pre, blockquote), без сплошного текста, дели текст на абзацы, между абзацами пустая строка."
    
    try:
        response = await chat.send_message(prompt)
        return response.text or ""
    except Exception as e:
        logger.exception("Ошибка Gemini для user_id=%s: %s", user_id, e)
        return f"Ошибка при обращении к ИИ: {e!s}"
