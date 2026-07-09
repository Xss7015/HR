from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import LanguageState, SurveyState
from bot.keyboards import get_language_keyboard, get_main_keyboard
from database import get_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await get_user(tg_id)
    
    if user and user.get('phone'):
        lang = user.get('language', 'russian')
        await state.update_data(language=lang, phone=user.get('phone'))
        await state.set_state(SurveyState.name)
        await message.answer(
            "👋 Здравствуйте!\n\nЯ HR-бот помощник по поиску работы.\n\n❓ *Как Вас зовут?*",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    await state.set_state(LanguageState.choosing_language)
    await message.answer(
        "🌍 Choose language / Выберите язык / בחר שפה:",
        reply_markup=get_language_keyboard()
    )