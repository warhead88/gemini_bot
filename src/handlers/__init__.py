from aiogram import Router
from .common import router as common_router
from .chat import router as chat_router

# Объединяем все роутеры в один
main_router = Router()
main_router.include_router(common_router)
main_router.include_router(chat_router)
