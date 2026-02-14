"""Загрузка конфигурации из .env и переменных окружения."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Путь к корню проекта (где лежит .env)
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


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

def get_redis_url() -> str:
    """URL Redis из REDIS_URL."""
    url = os.getenv("REDIS_URL")
    if not url:
        raise ValueError("REDIS_URL не задан в .env или окружении")
    return url