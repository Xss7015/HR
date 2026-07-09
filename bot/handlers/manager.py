from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🤖 *HR-бот*\n\n"
        "/start - начать анкету\n"
        "/admin - админ-панель (только для админов)\n"
        "/help - помощь",
        parse_mode="Markdown"
    )