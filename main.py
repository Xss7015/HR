import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db
from bot.handlers import start, language, survey, vacancies, admin, manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🚀 Запуск бота...")
    
    os.makedirs("data", exist_ok=True)
    await init_db()
    logger.info("✅ База данных инициализирована")
    
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(survey.router)
    dp.include_router(vacancies.router)
    dp.include_router(admin.router)
    dp.include_router(manager.router)
    
    logger.info("✅ Все роутеры зарегистрированы")
    
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Webhook удален")
    
    logger.info("✅ Бот запущен! Ожидаем сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")