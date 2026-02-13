"""Загрузка конфигурации из .env и переменных окружения."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Подгрузка .env из корня проекта
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


def get_bot_token() -> str:
    """Токен бота из BOT_TOKEN."""
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан в .env или окружении")
    return token


def get_gemini_api_key() -> str:
    """API-ключ Gemini из GEMINI_API_KEY."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY не задан в .env или окружении")
    return key
