from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from sessions.services.gemini_service import stop_chat

router = Router()

@router.message(Command("stop"))
async def cmd_stop(message: Message) -> None:
    """Завершение диалога с ИИ."""
    user_id = message.from_user.id if message.from_user else 0
    if stop_chat(user_id):
        await message.answer("Диалог завершён.")
    else:
        await message.answer("Диалог не был активен. Используйте /chat чтобы начать.")