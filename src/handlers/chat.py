import logging
import time
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.services.gemini import send_message_stream
from src.services.redis_storage import RedisStorage

logger = logging.getLogger(__name__)

router = Router(name="chat_logic")


@router.message(Command("chat"))
async def cmd_chat(message: Message, redis: RedisStorage):
    """Запуск диалога (создаем пустую историю в Redis)."""
    user_id = message.from_user.id if message.from_user else 0
    await redis.save_history(user_id, [])
    await message.answer(
        "Диалог с ИИ запущен. Пишите сообщения — я буду отвечать.\n"
        "Команда /stop завершит диалог."
    )


@router.message(Command("stop"))
async def cmd_stop(message: Message, redis: RedisStorage):
    """Завершение диалога (удаляем историю из Redis)."""
    user_id = message.from_user.id if message.from_user else 0
    history = await redis.get_history(user_id)
    if history or await redis.client.exists(f"chat:{user_id}"):
        await redis.clear_history(user_id)
        await message.answer("Диалог завершён.")
    else:
        await message.answer("Диалог не был активен. Используйте /chat чтобы начать.")


@router.message()
async def message_handler(message: Message, redis: RedisStorage):
    """Обработка текстовых сообщений с сохранением контекста в Redis."""
    user_id = message.from_user.id if message.from_user else 0
    text = message.text or message.caption
    
    if not text or not text.strip():
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    # 1. Получаем историю из Redis
    history = await redis.get_history(user_id)
    
    reply_full = ""
    last_edit_time = 0
    edit_interval = 1.0

    msg = await message.answer("🔍")
    
    try:
        # 2. Генерируем ответ, передавая историю
        async for chunk in send_message_stream(history, text.strip()):
            reply_full += chunk
            
            current_time = time.time()
            if current_time - last_edit_time > edit_interval:
                try:
                    await msg.edit_text(reply_full)
                    last_edit_time = current_time
                except Exception:
                    pass
        
        # Финальное обновление 
        await msg.edit_text(reply_full)

        # 3. Обновляем историю в Redis (добавляем юзера и ответ модели)
        history.append({"role": "user", "parts": [text.strip()]})
        history.append({"role": "model", "parts": [reply_full]})
        await redis.save_history(user_id, history)

    except Exception as e:
        logger.error(f"Error in streaming: {e}")
        await message.answer("Произошла ошибка при получении ответа.")