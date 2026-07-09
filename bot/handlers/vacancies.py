from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_change_visa_keyboard, get_main_keyboard
from bot.translations import get_text
from bot.utils import format_vacancies
from database import get_vacancies_by_visa, create_visa_request, save_dialog, get_user
from config import GROUP_LINK_RU, GROUP_LINK_EN, GROUP_LINK_HE, ADMIN_IDS
from bot.handlers.admin import notify_admins

router = Router()

def get_group_link_by_lang(lang: str) -> str:
    if lang == 'russian':
        return GROUP_LINK_RU
    elif lang == 'english':
        return GROUP_LINK_EN
    elif lang == 'hebrew':
        return GROUP_LINK_HE
    return GROUP_LINK_RU

async def get_user_language(tg_id: int) -> str:
    user = await get_user(tg_id)
    return user.get('language', 'russian') if user else 'russian'

async def handle_vacancies(message: Message, state: FSMContext, lang: str, visa: str):
    """Основная логика проверки вакансий (БЫСТРАЯ)"""
    tg_id = message.from_user.id
    
    # Если виза не указана ("Другое") — сразу отправляем группу
    if not visa or visa == '':
        await message.answer(
            get_text(lang, 'no_vacancies_at_all'),
            parse_mode="Markdown",
            reply_markup=get_main_keyboard(tg_id, lang)
        )
        group_link = get_group_link_by_lang(lang)
        await message.answer(
            get_text(lang, 'group_message', group_link=group_link),
            parse_mode="Markdown"
        )
        await state.clear()
        return
    
    # Ищем вакансии по визе (ОДИН ЗАПРОС)
    vacancies = await get_vacancies_by_visa(visa)
    
    if vacancies:
        vac_text = format_vacancies(vacancies)
        await message.answer(
            get_text(lang, 'vacancies_found', vacancies=vac_text),
            parse_mode="Markdown",
            reply_markup=get_main_keyboard(tg_id, lang)
        )
        group_link = get_group_link_by_lang(lang)
        await message.answer(
            get_text(lang, 'group_message', group_link=group_link),
            parse_mode="Markdown"
        )
        await state.clear()
        return
    
    # Нет вакансий
    await message.answer(
        get_text(lang, 'no_vacancies'),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Предлагаем смену визы
    await state.set_state('change_visa')
    await state.update_data(visa=visa)
    await message.answer(
        get_text(lang, 'change_visa_question'),
        reply_markup=get_change_visa_keyboard(lang)
    )

# ============ ОБРАБОТЧИКИ СМЕНЫ ВИЗЫ ============

@router.message(F.text.in_(["✅ Да", "✅ Yes", "✅ כן"]))
async def change_visa_yes(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    tg_id = message.from_user.id
    data = await state.get_data()
    visa = data.get('visa', '')
    
    await create_visa_request(tg_id, visa)
    
    user = await get_user(tg_id)
    await notify_admins(
        tg_id=tg_id,
        name=user.get('name', '') if user else '',
        phone=user.get('phone', '') if user else '',
        visa=f"{visa} → запрос на смену"
    )
    
    await message.answer(
        get_text(lang, 'visa_change_requested'),
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(tg_id, lang)
    )
    
    group_link = get_group_link_by_lang(lang)
    await message.answer(
        get_text(lang, 'group_message', group_link=group_link),
        parse_mode="Markdown"
    )
    
    await state.clear()

@router.message(F.text.in_(["❌ Нет", "❌ No", "❌ לא"]))
async def change_visa_no(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    tg_id = message.from_user.id
    data = await state.get_data()
    visa = data.get('visa', '')
    
    await message.answer(
        get_text(lang, 'visa_change_declined'),
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(tg_id, lang)
    )
    
    group_link = get_group_link_by_lang(lang)
    await message.answer(
        get_text(lang, 'group_message', group_link=group_link),
        parse_mode="Markdown"
    )
    
    await state.clear()