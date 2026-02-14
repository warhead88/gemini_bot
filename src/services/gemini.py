"""Сервис для диалога с моделью Gemini (Google GenAI SDK)."""

import logging
from typing import Any, AsyncGenerator, List
from google import genai
from src.core.config import get_gemini_api_key

logger = logging.getLogger(__name__)

# Модель по умолчанию
GEMINI_MODEL = "gemini-2.5-flash"


def _get_client() -> genai.Client:
    """Возвращает клиент GenAI."""
    return genai.Client(api_key=get_gemini_api_key())


async def send_message_stream(history: List[dict], text: str) -> AsyncGenerator[str, None]:
    """
    Отправляет сообщение, используя переданную историю.
    history — список сообщений в формате Gemini (role, parts).
    """
    client = _get_client()
    
    config = genai.types.GenerateContentConfig(
        response_schema=None,
        system_instruction=(
            "Отвечай на русском языке в формате HTML (только эти теги: b, i, u, s, code, pre, blockquote), другие теги использовать нельзя!"
            "без сплошного текста, дели текст на абзацы, между абзацами пустая строка."
        )
    )
    
    try:
        # Создаем временный объект чата с переданной историей
        chat = client.aio.chats.create(model=GEMINI_MODEL, history=history, config=config)
        
        response = await chat.send_message_stream(text)
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        logger.exception("Ошибка Gemini: %s", e)
        yield f"Ошибка при обращении к ИИ: {e!s}"