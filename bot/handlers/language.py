from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import LanguageState, SurveyState
from bot.keyboards import get_phone_keyboard
from bot.translations import get_text
from database import save_user_language

router = Router()

@router.callback_query(F.data.startswith("lang_"), LanguageState.choosing_language)
async def select_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    
    await save_user_language(callback.from_user.id, lang)
    await state.update_data(language=lang)
    await state.set_state(SurveyState.phone)
    
    await callback.message.delete()
    await callback.message.answer(
        get_text(lang, 'phone_request'),
        reply_markup=get_phone_keyboard(lang)
    )
    await callback.answer()