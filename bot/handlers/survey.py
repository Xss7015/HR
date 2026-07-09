from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, Contact, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import re
import logging

from bot.states import SurveyState
from bot.keyboards import (
    get_phone_keyboard,
    get_document_keyboard,
    get_visa_keyboard,
    get_main_keyboard,
    get_back_keyboard
)
from bot.translations import get_text
from database import (
    save_user_phone,
    save_user,
    save_user_visa,
    get_user_language,
    get_user,
    save_user_name
)
from bot.handlers.vacancies import handle_vacancies
from bot.handlers.admin import notify_admins

router = Router()
logger = logging.getLogger(__name__)


@router.message(StateFilter(SurveyState.phone))
async def process_phone(message: Message, state: FSMContext):
    """Обработка номера телефона"""
    tg_id = message.from_user.id
    lang = await get_user_language(tg_id)

    try:
        if message.contact:
            phone = message.contact.phone_number
            await save_user_phone(tg_id, phone)
            await state.update_data(phone=phone)

            await message.answer(
                get_text(lang, 'phone_saved'),
                reply_markup=ReplyKeyboardRemove()
            )

            await state.set_state(SurveyState.name)
            await message.answer(
                get_text(lang, 'greeting'),
                parse_mode="Markdown"
            )
        else:
            await message.answer(
                get_text(lang, 'phone_error'),
                reply_markup=get_phone_keyboard(lang)
            )
    except Exception as e:
        logger.error(f"Ошибка при сохранении телефона: {e}")
        await message.answer(
            "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
            reply_markup=get_phone_keyboard(lang)
        )


@router.message(StateFilter(SurveyState.name))
async def process_name(message: Message, state: FSMContext):
    """Обработка имени пользователя"""
    tg_id = message.from_user.id
    lang = await get_user_language(tg_id)
    name = message.text.strip()

    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-\.\']+$', name):
        await message.answer(get_text(lang, 'name_error'))
        return

    if len(name) < 2:
        await message.answer(get_text(lang, 'name_short'))
        return

    await state.update_data(name=name)
    await save_user_name(tg_id, name)

    data = await state.get_data()
    phone = data.get('phone', '')
    user = await get_user(tg_id)

    if not user:
        await save_user(tg_id, lang, phone, name)
    else:
        await save_user(tg_id, lang, user.get('phone', ''), name)

    await state.set_state(SurveyState.document)
    await message.answer(
        get_text(lang, 'doc_question'),
        parse_mode="Markdown",
        reply_markup=get_document_keyboard(lang)
    )


@router.message(StateFilter(SurveyState.document))
async def process_document(message: Message, state: FSMContext):
    """Обработка выбора документа"""
    tg_id = message.from_user.id
    lang = await get_user_language(tg_id)
    doc_text = message.text.strip()

    valid_docs = [
        get_text(lang, 'doc_visa'),
        get_text(lang, 'doc_id'),
        get_text(lang, 'doc_other')
    ]

    # Если нажал "Назад" — возвращаемся к имени
    if doc_text == get_text(lang, 'back'):
        await state.set_state(SurveyState.name)
        await message.answer(
            get_text(lang, 'enter_name'),
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    if doc_text not in valid_docs:
        await message.answer(
            get_text(lang, 'choose_from_buttons'),
            reply_markup=get_document_keyboard(lang)
        )
        return

    await state.update_data(document=doc_text)

    # Если выбрали "Другое" — ПРОПУСКАЕМ ВИЗУ!
    if doc_text == get_text(lang, 'doc_other'):
        data = await state.get_data()
        await notify_admins(
            tg_id=tg_id,
            name=data.get('name', ''),
            phone=data.get('phone', ''),
            visa="Другое (документ не указан)"
        )
        await handle_vacancies(message, state, lang, "")
        return

    # Если выбрали визу или ID — спрашиваем тип визы
    await state.set_state(SurveyState.visa)
    await message.answer(
        get_text(lang, 'visa_question'),
        parse_mode="Markdown",
        reply_markup=get_visa_keyboard(lang)
    )


@router.message(StateFilter(SurveyState.visa))
async def process_visa(message: Message, state: FSMContext):
    """Обработка выбора визы"""
    tg_id = message.from_user.id
    lang = await get_user_language(tg_id)
    visa = message.text.strip()

    # Если нажал "Назад" — возвращаемся к документу
    if visa == get_text(lang, 'back'):
        await state.set_state(SurveyState.document)
        await message.answer(
            get_text(lang, 'doc_question'),
            parse_mode="Markdown",
            reply_markup=get_document_keyboard(lang)
        )
        return

    valid_visas = [
        'B/1', 'B/2', 'A/5', 'A/2',
        get_text(lang, 'visa_refugee'),
        get_text(lang, 'visa_blue_paper'),
        get_text(lang, 'visa_other')
    ]

    if visa not in valid_visas:
        await message.answer(
            get_text(lang, 'choose_from_buttons'),
            reply_markup=get_visa_keyboard(lang)
        )
        return

    await save_user_visa(tg_id, visa)
    await state.update_data(visa=visa)

    data = await state.get_data()
    await notify_admins(
        tg_id=tg_id,
        name=data.get('name', ''),
        phone=data.get('phone', ''),
        visa=visa
    )

    await handle_vacancies(message, state, lang, visa)