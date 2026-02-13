from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот с ИИ-агентом на базе Gemini.\n\n"
        "Команды:\n"
        "/chat — начать диалог с ИИ\n"
        "/stop — завершить диалог"
    )