import sqlite3
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext

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

# ========== ХЕНДЛЕР КОМАНДЫ /START ==========
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    save_user(message)
    await message.answer("👋 Привет! Ты уже в базе. Отправь /phone чтобы сохранить номер.")

# ========== ХЕНДЛЕР ДЛЯ НОМЕРА ТЕЛЕФОНА ==========
@dp.message_handler(commands=['phone'])
async def ask_phone(message: types.Message):
    # Создаём кнопку с запросом номера
    button = types.KeyboardButton("📱 Отправить номер", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await message.answer("Нажми на кнопку, чтобы поделиться номером", reply_markup=keyboard)

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message, state: FSMContext):
    if message.contact is not None:
        phone = message.contact.phone_number
        user_id = message.from_user.id
        update_user_phone(user_id, phone)
        await message.answer(f"✅ Номер {phone} сохранён! Спасибо.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("❌ Пожалуйста, используй кнопку 'Отправить номер'.")