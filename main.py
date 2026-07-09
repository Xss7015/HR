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

# ========== ЗАГРУЖАЕМ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ==========
load_dotenv()  # Загружаем .env
TOKEN = os.getenv("BOT_TOKEN")  # Берём токен из переменной

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
    logging.info(f"✅ Номер {phone} сохранён для user_id={user_id}")

# ========== СОСТОЯНИЯ ==========
class UserState(StatesGroup):
    waiting_for_phone = State()

# ========== ХЕНДЛЕРЫ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    save_user(message)
    await message.answer("👋 Привет! Ты уже в базе. Отправь /phone, чтобы сохранить номер.")

@dp.message(Command("phone"))
async def ask_phone(message: types.Message, state: FSMContext):
    button = KeyboardButton("📱 Отправить номер", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    await state.set_state(UserState.waiting_for_phone)
    await message.answer("Нажми на кнопку, чтобы поделиться номером", reply_markup=keyboard)

@dp.message(UserState.waiting_for_phone, lambda msg: msg.contact is not None)
async def handle_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    update_user_phone(user_id, phone)
    await state.clear()
    await message.answer(f"✅ Номер {phone} сохранён! Спасибо.", reply_markup=ReplyKeyboardRemove())

@dp.message(UserState.waiting_for_phone)
async def timeout_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("⏰ Ты не отправил номер. Начни заново с /phone", reply_markup=ReplyKeyboardRemove())

# ========== ЗАПУСК ==========
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    init_db()
    logging.info("🚀 Запуск бота...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())