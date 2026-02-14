import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.services.gemini import start_chat, stop_chat, is_chat_active, send_message

logger = logging.getLogger(__name__)

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
    
    # Middleware уже проверил, что чат активен — здесь можно просто работать с Gemini
    text = message.text or message.caption
    if not text or not text.strip():
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    import time
    
    reply = ""
    last_edit_time = 0
    edit_interval = 1.0  # Секунда между редактированиями

    msg = await message.answer("🔍")
    
    try:
        async for chunk in send_message(user_id, text.strip()):
            reply += chunk
            
            # Редактируем сообщение только если прошло достаточно времени
            current_time = time.time()
            if current_time - last_edit_time > edit_interval:
                try:
                    await msg.edit_text(reply)
                    last_edit_time = current_time
                except Exception:
                    # Игнорируем ошибки редактирования (например, если текст не изменился)
                    pass
        
        # Финальное обновление после завершения генерации
        try:
            await msg.edit_text(reply)
        except:
            pass

    except Exception as e:
        logger.error(f"Error in streaming: {e}")
        await message.answer("Произошла ошибка при получении ответа.")