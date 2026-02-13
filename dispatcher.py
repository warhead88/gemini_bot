"""Роутер с обработчиками команд и сообщений."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from sessions.services.gemini_service import is_chat_active, send_message, start_chat, stop_chat

router = Router(name="main")

@router.message(Command("stop"))
async def cmd_stop(message: Message) -> None:
    """Завершение диалога с ИИ."""
    user_id = message.from_user.id if message.from_user else 0
    if stop_chat(user_id):
        await message.answer("Диалог завершён.")
    else:
        await message.answer("Диалог не был активен. Используйте /chat чтобы начать.")


@router.message()
async def message_handler(message: Message) -> None:
    """Обработка сообщений: в режиме чата — отправка в Gemini, иначе подсказка."""
    user_id = message.from_user.id if message.from_user else 0
    if not is_chat_active(user_id):
        await message.answer("Используйте /chat чтобы начать диалог с ИИ.")
        return
    text = message.text or message.caption
    if not text or not text.strip():
        await message.answer("В режиме чата принимаются только текстовые сообщения.")
        return
    reply = await send_message(user_id, text.strip())
    await message.answer(reply or "Нет ответа от модели.")
