from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="common_commands")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик /start."""
    await message.answer(
        "Привет! Я бот с ИИ-агентом на базе Gemini.\n\n"
        "Команды:\n"
        "/chat — начать диалог с ИИ\n"
        "/stop — завершить диалог"
    )
