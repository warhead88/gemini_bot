from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from sessions.services.gemini_service import start_chat

router = Router()

@router.message(Command("chat"))
async def cmd_chat(message: Message) -> None:
    """Запуск диалога с ИИ."""
    user_id = message.from_user.id if message.from_user else 0
    start_chat(user_id)
    await message.answer(
        "Диалог с ИИ запущен. Пишите сообщения — бот будет отвечать от имени агента.\n"
        "Команда /stop завершит диалог."
    )