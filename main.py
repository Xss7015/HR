import os
import logging
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import asyncio

# ========== ЗАГРУЖАЕМ ПЕРЕМЕННЫЕ ==========
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Проверь .env файл.")

# ========== НАСТРОЙКИ ==========
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ========== БАЗА ДАННЫХ ==========
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  last_name TEXT,
                  phone TEXT,
                  registered_at TEXT)''')
    conn.commit()
    conn.close()
    logging.info("✅ База данных инициализирована")

def save_user(message: types.Message):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, registered_at)
                 VALUES (?, ?, ?, ?, ?)''',
              (message.from_user.id,
               message.from_user.username,
               message.from_user.first_name,
               message.from_user.last_name,
               datetime.now().isoformat()))
    conn.commit()
    conn.close()

def update_user_phone(user_id: int, phone: str):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET phone = ? WHERE user_id = ?', (phone, user_id))
    conn.commit()
    conn.close()
    logging.info(f"✅ Номер {phone} сохранён")

# ========== FSM ==========
class Form(StatesGroup):
    waiting_phone = State()

# ========== КОМАНДА /START ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    save_user(message)
    await message.answer(
        "👋 Привет! Я бот для сбора номеров телефонов.\n\n"
        "Отправь /phone, чтобы поделиться номером."
    )

# ========== КОМАНДА /PHONE ==========
@dp.message(Command("phone"))
async def cmd_phone(message: types.Message, state: FSMContext):
    # Правильный способ создать кнопку с запросом контакта в aiogram 3.x
    button = KeyboardButton(text="📱 Отправить номер", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    
    await state.set_state(Form.waiting_phone)
    await message.answer(
        "Нажми на кнопку ниже, чтобы отправить свой номер телефона:",
        reply_markup=keyboard
    )

# ========== ОБРАБОТКА КОНТАКТА ==========
@dp.message(Form.waiting_phone, lambda message: message.contact is not None)
async def process_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    update_user_phone(user_id, phone)
    
    await state.clear()
    await message.answer(
        f"✅ Номер {phone} успешно сохранён!",
        reply_markup=ReplyKeyboardRemove()
    )

# ========== ОБРАБОТКА ТЕКСТА В СОСТОЯНИИ ==========
@dp.message(Form.waiting_phone)
async def process_phone_invalid(message: types.Message, state: FSMContext):
    await message.answer(
        "⚠️ Пожалуйста, используй кнопку '📱 Отправить номер' для отправки контакта.\n\n"
        "Если кнопка не отображается, отправь /phone заново."
    )

# ========== ЗАПУСК ==========
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    init_db()
    logging.info("🚀 Запуск бота...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())