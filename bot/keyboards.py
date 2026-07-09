from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_russian")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_english")],
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_hebrew")]
    ])

def get_phone_keyboard(lang: str):
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, 'send_phone'), request_contact=True)]
        ],
        resize_keyboard=True
    )

def get_document_keyboard(lang: str):
    """Клавиатура выбора документа (С КНОПКОЙ НАЗАД)"""
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, 'doc_visa')), KeyboardButton(text=get_text(lang, 'doc_id'))],
            [KeyboardButton(text=get_text(lang, 'doc_other'))],
            [KeyboardButton(text=f"⬅️ {get_text(lang, 'back')}")]
        ],
        resize_keyboard=True
    )

def get_visa_keyboard(lang: str):
    """Клавиатура выбора визы (С КНОПКОЙ НАЗАД)"""
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="B/1"), KeyboardButton(text="B/2")],
            [KeyboardButton(text="A/5"), KeyboardButton(text="A/2")],
            [KeyboardButton(text=get_text(lang, 'visa_refugee')), KeyboardButton(text=get_text(lang, 'visa_blue_paper'))],
            [KeyboardButton(text=get_text(lang, 'visa_other'))],
            [KeyboardButton(text=f"⬅️ {get_text(lang, 'back')}")]
        ],
        resize_keyboard=True
    )

def get_change_visa_keyboard(lang: str):
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, 'yes')), KeyboardButton(text=get_text(lang, 'no'))]
        ],
        resize_keyboard=True
    )

def get_admin_keyboard(lang: str):
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"👤 {get_text(lang, 'admin_candidates')}")],
            [KeyboardButton(text=f"📋 {get_text(lang, 'admin_vacancies')}")],
            [KeyboardButton(text=f"➕ {get_text(lang, 'admin_add')}")],
            [KeyboardButton(text=f"✏️ {get_text(lang, 'admin_edit')}")],
            [KeyboardButton(text=f"🗑 {get_text(lang, 'admin_delete')}")],
            [KeyboardButton(text=f"📊 {get_text(lang, 'admin_requests')}")],
            [KeyboardButton(text=f"❌ {get_text(lang, 'admin_close')}")]
        ],
        resize_keyboard=True
    )

def get_main_keyboard(tg_id: int, lang: str):
    from bot.translations import get_text
    buttons = [
        [KeyboardButton(text=get_text(lang, 'vacancies_btn'))],
        [KeyboardButton(text=get_text(lang, 'help_btn'))]
    ]
    if tg_id in ADMIN_IDS:
        buttons.append([KeyboardButton(text=get_text(lang, 'admin_btn'))])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

def get_visa_list_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="B/1"), KeyboardButton(text="B/2")],
            [KeyboardButton(text="A/5"), KeyboardButton(text="A/2")],
            [KeyboardButton(text="Refugee"), KeyboardButton(text="Blue Paper")],
            [KeyboardButton(text="Other")]
        ],
        resize_keyboard=True
    )

def get_skip_keyboard(lang: str):
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, 'skip'))]
        ],
        resize_keyboard=True
    )

def get_back_keyboard(lang: str):
    """Клавиатура только с кнопкой "Назад" (для универсальности)"""
    from bot.translations import get_text
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"⬅️ {get_text(lang, 'back')}")]
        ],
        resize_keyboard=True
    )