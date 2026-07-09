from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from datetime import datetime
import logging

from config import ADMIN_IDS, BOT_TOKEN
from bot.states import SurveyState
from bot.keyboards import get_admin_keyboard, get_visa_list_keyboard, get_skip_keyboard, get_main_keyboard
from bot.translations import get_text
from bot.utils import format_admin_vacancies, format_visa_requests, format_candidates_list
from database import (
    get_user_language, get_all_vacancies, add_vacancy, 
    delete_vacancy, get_vacancy, update_vacancy,
    get_all_visa_requests, get_user, get_all_users
)

router = Router()
logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

def is_admin(tg_id: int) -> bool:
    return tg_id in ADMIN_IDS

async def notify_admins(tg_id: int, name: str, phone: str, visa: str):
    if not ADMIN_IDS:
        return
    
    text = (
        f"🔔 *НОВЫЙ КАНДИДАТ!*\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"🛂 Виза: {visa}\n"
        f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление админу {admin_id}: {e}")

# ============ АДМИН-ПАНЕЛЬ ============

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        lang = await get_user_language(message.from_user.id)
        await message.answer(get_text(lang, 'admin_access_denied'))
        return
    
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        get_text(lang, 'admin_panel'),
        reply_markup=get_admin_keyboard(lang)
    )

# ============ КАНДИДАТЫ ============

@router.message(F.text.contains("👤 Кандидаты"))
async def admin_candidates(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    users = await get_all_users()
    
    if not users:
        await message.answer(get_text(lang, 'admin_no_candidates'))
        return
    
    text = format_candidates_list(users)
    await message.answer(
        get_text(lang, 'admin_candidates_list', candidates=text),
        parse_mode="Markdown"
    )

# ============ ВАКАНСИИ ============

@router.message(F.text.contains("📋 Вакансии"))
async def admin_vacancies(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    vacancies = await get_all_vacancies()
    
    if not vacancies:
        await message.answer(get_text(lang, 'admin_no_vacancies'))
        return
    
    text = format_admin_vacancies(vacancies)
    await message.answer(
        get_text(lang, 'admin_vacancies_list', vacancies=text),
        parse_mode="Markdown"
    )

# ============ ДОБАВЛЕНИЕ ============

@router.message(F.text.contains("➕ Добавить"))
async def admin_add_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    await state.set_state(SurveyState.add_vacancy_title)
    await message.answer(
        get_text(lang, 'admin_add_title'),
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(StateFilter(SurveyState.add_vacancy_title))
async def admin_add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    lang = await get_user_language(message.from_user.id)
    await state.set_state(SurveyState.add_vacancy_description)
    await message.answer(get_text(lang, 'admin_add_description'))

@router.message(StateFilter(SurveyState.add_vacancy_description))
async def admin_add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    lang = await get_user_language(message.from_user.id)
    await state.set_state(SurveyState.add_vacancy_photo)
    await message.answer(
        get_text(lang, 'admin_add_photo'),
        reply_markup=get_skip_keyboard(lang)
    )

@router.message(StateFilter(SurveyState.add_vacancy_photo))
async def admin_add_photo(message: Message, state: FSMContext):
    photo_id = ''
    if message.photo:
        photo_id = message.photo[-1].file_id
    
    await state.update_data(photo_id=photo_id)
    lang = await get_user_language(message.from_user.id)
    await state.set_state(SurveyState.add_vacancy_visa)
    await message.answer(
        get_text(lang, 'admin_add_visa'),
        reply_markup=get_visa_list_keyboard()
    )

@router.message(StateFilter(SurveyState.add_vacancy_visa))
async def admin_add_visa(message: Message, state: FSMContext):
    data = await state.get_data()
    vacancy_id = await add_vacancy(
        title=data['title'],
        description=data['description'],
        photo_id=data.get('photo_id', ''),
        visa_type=message.text
    )
    
    lang = await get_user_language(message.from_user.id)
    tg_id = message.from_user.id
    await message.answer(
        get_text(lang, 'admin_add_success', vacancy_id=vacancy_id),
        reply_markup=get_admin_keyboard(lang)
    )
    await state.clear()

# ============ УДАЛЕНИЕ ============

@router.message(F.text.contains("🗑 Удалить"))
async def admin_delete_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    await state.set_state(SurveyState.delete_vacancy)
    await message.answer(
        get_text(lang, 'admin_delete_ask_id'),
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(StateFilter(SurveyState.delete_vacancy))
async def admin_delete(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    tg_id = message.from_user.id
    
    try:
        vacancy_id = int(message.text)
        await delete_vacancy(vacancy_id)
        await message.answer(
            get_text(lang, 'admin_delete_success'),
            reply_markup=get_admin_keyboard(lang)
        )
    except ValueError:
        await message.answer("❌ Введите число (ID вакансии)")
    
    await state.clear()

# ============ РЕДАКТИРОВАНИЕ ============

@router.message(F.text.contains("✏️ Редактировать"))
async def admin_edit_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    await state.set_state(SurveyState.edit_vacancy_id)
    await message.answer(
        get_text(lang, 'admin_edit_ask_id'),
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(StateFilter(SurveyState.edit_vacancy_id))
async def admin_edit_id(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    
    try:
        vacancy_id = int(message.text)
        vacancy = await get_vacancy(vacancy_id)
        
        if not vacancy:
            await message.answer(get_text(lang, 'admin_edit_not_found'))
            return
        
        await state.update_data(edit_id=vacancy_id)
        await state.set_state(SurveyState.edit_vacancy_title)
        await message.answer(
            get_text(lang, 'admin_edit_title'),
            reply_markup=get_skip_keyboard(lang)
        )
    except ValueError:
        await message.answer("❌ Введите число (ID вакансии)")

@router.message(StateFilter(SurveyState.edit_vacancy_title))
async def admin_edit_title(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    if message.text != get_text(lang, 'skip'):
        await state.update_data(edit_title=message.text)
    await state.set_state(SurveyState.edit_vacancy_description)
    await message.answer(get_text(lang, 'admin_edit_description'), reply_markup=get_skip_keyboard(lang))

@router.message(StateFilter(SurveyState.edit_vacancy_description))
async def admin_edit_description(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    if message.text != get_text(lang, 'skip'):
        await state.update_data(edit_description=message.text)
    await state.set_state(SurveyState.edit_vacancy_photo)
    await message.answer(get_text(lang, 'admin_edit_photo'), reply_markup=get_skip_keyboard(lang))

@router.message(StateFilter(SurveyState.edit_vacancy_photo))
async def admin_edit_photo(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    if message.text != get_text(lang, 'skip') and message.photo:
        await state.update_data(edit_photo_id=message.photo[-1].file_id)
    await state.set_state(SurveyState.edit_vacancy_visa)
    await message.answer(get_text(lang, 'admin_edit_visa'), reply_markup=get_skip_keyboard(lang))

@router.message(StateFilter(SurveyState.edit_vacancy_visa))
async def admin_edit_visa(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    tg_id = message.from_user.id
    data = await state.get_data()
    
    update_data = {}
    if data.get('edit_title'):
        update_data['title'] = data['edit_title']
    if data.get('edit_description'):
        update_data['description'] = data['edit_description']
    if data.get('edit_photo_id'):
        update_data['photo_id'] = data['edit_photo_id']
    if message.text != get_text(lang, 'skip'):
        update_data['visa_type'] = message.text
    
    if update_data:
        await update_vacancy(data['edit_id'], update_data)
        await message.answer(get_text(lang, 'admin_edit_success'))
    else:
        await message.answer("ℹ️ Ничего не изменено")
    
    await message.answer(
        get_text(lang, 'admin_panel'),
        reply_markup=get_admin_keyboard(lang)
    )
    await state.clear()

# ============ ЗАЯВКИ ============

@router.message(F.text.contains("📊 Заявки"))
async def admin_requests(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    requests = await get_all_visa_requests()
    
    if not requests:
        await message.answer(get_text(lang, 'admin_no_requests'))
        return
    
    text = format_visa_requests(requests)
    await message.answer(
        get_text(lang, 'admin_requests_list', requests=text),
        parse_mode="Markdown"
    )

# ============ ЗАКРЫТИЕ ============

@router.message(F.text.contains("❌ Закрыть"))
async def admin_close(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    lang = await get_user_language(message.from_user.id)
    tg_id = message.from_user.id
    await message.answer(
        get_text(lang, 'admin_closed'),
        reply_markup=get_main_keyboard(tg_id, lang)
    )