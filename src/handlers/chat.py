from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.services.gemini import start_chat, stop_chat, is_chat_active, send_message

router = Router(name="chat_logic")


@router.message(Command("chat"))
async def cmd_chat(message: Message):
    """Запуск диалога."""
    user_id = message.from_user.id if message.from_user else 0
    start_chat(user_id)
    await message.answer(
        "Диалог с ИИ запущен. Пишите сообщения — я буду отвечать.\n"
        "Команда /stop завершит диалог."
    )


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    """Завершение диалога."""
    user_id = message.from_user.id if message.from_user else 0
    if stop_chat(user_id):
        await message.answer("Диалог завершён.")
    else:
        await message.answer("Диалог не был активен. Используйте /chat чтобы начать.")


@router.message()
async def message_handler(message: Message):
    """Обработка текстовых сообщений."""
    user_id = message.from_user.id if message.from_user else 0
    
    if not is_chat_active(user_id):
        await message.answer("Чтобы пообщаться с ИИ, сначала введите команду /chat")
        return

    text = message.text or message.caption
    if not text or not text.strip():
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    reply = await send_message(user_id, text.strip())
    await message.answer(reply or "Извините, я не смог сформулировать ответ.")
