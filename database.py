import aiosqlite
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

DB_PATH = "data/hr_bot.db"
logger = logging.getLogger(__name__)


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица пользователей
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'russian',
                phone TEXT DEFAULT '',
                name TEXT DEFAULT '',
                visa_type TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Добавляем колонки если их нет
        for col in ['name', 'phone', 'visa_type']:
            try:
                await db.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT ''")
                logger.info(f"✅ Колонка {col} добавлена в таблицу users")
            except sqlite3.OperationalError:
                pass

        # Таблица вакансий
        await db.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                photo_id TEXT,
                visa_type TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица заявок на смену визы
        await db.execute("""
            CREATE TABLE IF NOT EXISTS visa_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                current_visa TEXT,
                requested_visa TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tg_id) REFERENCES users(tg_id)
            )
        """)

        # Таблица диалогов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dialogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                message TEXT,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tg_id) REFERENCES users(tg_id)
            )
        """)

        await db.commit()
        logger.info("✅ База данных инициализирована")


# ============ РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ============

async def get_user(tg_id: int) -> Optional[Dict]:
    """Получить пользователя по tg_id"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE tg_id = ?", (tg_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def save_user(tg_id: int, language: str = 'russian', phone: str = '', name: str = '', visa_type: str = ''):
    """Сохранить или обновить пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (tg_id, language, phone, name, visa_type)
            VALUES (?, ?, ?, ?, ?)
        """, (tg_id, language, phone, name, visa_type))
        await db.commit()


async def save_user_language(tg_id: int, language: str):
    """Сохранить язык пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET language = ? WHERE tg_id = ?
        """, (language, tg_id))
        await db.commit()


async def save_user_phone(tg_id: int, phone: str):
    """Сохранить номер телефона пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET phone = ? WHERE tg_id = ?
        """, (phone, tg_id))
        await db.commit()


async def save_user_name(tg_id: int, name: str):
    """Сохранить имя пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET name = ? WHERE tg_id = ?
        """, (name, tg_id))
        await db.commit()


async def save_user_visa(tg_id: int, visa_type: str):
    """Сохранить тип визы пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET visa_type = ? WHERE tg_id = ?
        """, (visa_type, tg_id))
        await db.commit()


async def get_user_language(tg_id: int) -> str:
    """Получить язык пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT language FROM users WHERE tg_id = ?", (tg_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else 'russian'


async def get_user_phone(tg_id: int) -> str:
    """Получить номер телефона пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT phone FROM users WHERE tg_id = ?", (tg_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else ''


async def get_user_name(tg_id: int) -> str:
    """Получить имя пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT name FROM users WHERE tg_id = ?", (tg_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else ''


async def get_user_visa(tg_id: int) -> str:
    """Получить тип визы пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT visa_type FROM users WHERE tg_id = ?", (tg_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else ''


async def get_all_users() -> List[Dict]:
    """Получить всех пользователей"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


# ============ РАБОТА С ВАКАНСИЯМИ ============

async def add_vacancy(title: str, description: str, photo_id: str = '', visa_type: str = '') -> int:
    """Добавить вакансию"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO vacancies (title, description, photo_id, visa_type)
            VALUES (?, ?, ?, ?)
        """, (title, description, photo_id, visa_type))
        await db.commit()
        return cursor.lastrowid


async def get_vacancy(vacancy_id: int) -> Optional[Dict]:
    """Получить вакансию по ID"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vacancies WHERE id = ? AND is_active = 1", (vacancy_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_all_vacancies() -> List[Dict]:
    """Получить все активные вакансии"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vacancies WHERE is_active = 1 ORDER BY id"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_vacancies_by_visa(visa_type: str) -> List[Dict]:
    """Получить вакансии по типу визы"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vacancies WHERE visa_type = ? AND is_active = 1 ORDER BY id",
            (visa_type,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def update_vacancy(vacancy_id: int, data: Dict[str, Any]):
    """Обновить вакансию"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE vacancies 
            SET title = ?, description = ?, photo_id = ?, visa_type = ?
            WHERE id = ?
        """, (
            data.get('title'),
            data.get('description'),
            data.get('photo_id', ''),
            data.get('visa_type'),
            vacancy_id
        ))
        await db.commit()


async def delete_vacancy(vacancy_id: int):
    """Удалить вакансию (soft delete)"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE vacancies SET is_active = 0 WHERE id = ?", (vacancy_id,)
        )
        await db.commit()


# ============ РАБОТА С ЗАЯВКАМИ НА СМЕНУ ВИЗЫ ============

async def create_visa_request(tg_id: int, current_visa: str, requested_visa: str = '') -> int:
    """Создать заявку на смену визы"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO visa_requests (tg_id, current_visa, requested_visa)
            VALUES (?, ?, ?)
        """, (tg_id, current_visa, requested_visa))
        await db.commit()
        return cursor.lastrowid


async def get_all_visa_requests() -> List[Dict]:
    """Получить все активные заявки на смену визы"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT vr.*, u.name, u.phone 
            FROM visa_requests vr
            JOIN users u ON vr.tg_id = u.tg_id
            WHERE vr.status = 'pending'
            ORDER BY vr.created_at DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def update_visa_request_status(request_id: int, status: str):
    """Обновить статус заявки на смену визы"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE visa_requests SET status = ? WHERE id = ?
        """, (status, request_id))
        await db.commit()


# ============ РАБОТА С ДИАЛОГАМИ ============

async def save_dialog(tg_id: int, message: str, response: str):
    """Сохранить диалог"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO dialogs (tg_id, message, response)
            VALUES (?, ?, ?)
        """, (tg_id, message, response))
        await db.commit()


async def get_user_dialogs(tg_id: int, limit: int = 50) -> List[Dict]:
    """Получить диалоги пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM dialogs 
            WHERE tg_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (tg_id, limit))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_all_dialogs(limit: int = 100) -> List[Dict]:
    """Получить все диалоги"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM dialogs 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


# ============ СТАТИСТИКА ============

async def get_statistics() -> Dict[str, int]:
    """Получить статистику по базе"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Количество пользователей
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        users_count = (await cursor.fetchone())[0]

        # Количество вакансий
        cursor = await db.execute("SELECT COUNT(*) FROM vacancies WHERE is_active = 1")
        vacancies_count = (await cursor.fetchone())[0]

        # Количество заявок на смену визы
        cursor = await db.execute("SELECT COUNT(*) FROM visa_requests WHERE status = 'pending'")
        requests_count = (await cursor.fetchone())[0]

        return {
            'users': users_count,
            'vacancies': vacancies_count,
            'visa_requests': requests_count
        }


# ============ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ============

async def clear_old_data(days: int = 30):
    """Удалить старые диалоги"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            DELETE FROM dialogs 
            WHERE created_at < datetime('now', ?)
        """, (f"-{days} days",))
        await db.commit()


async def get_database_size() -> int:
    """Получить размер базы данных в байтах"""
    import os
    if os.path.exists(DB_PATH):
        return os.path.getsize(DB_PATH)
    return 0


async def vacuum_database():
    """Оптимизировать базу данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("VACUUM")
        await db.commit()


async def create_backup(backup_path: str):
    """Создать резервную копию базы данных"""
    import shutil
    import os
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, backup_path)
        return True
    return False