import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import WebhookInfo
from aiogram.webhook.aiohttp_server import SimpleWebhookResponse, setup_application

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT, WEBHOOK_PATH
from database import init_db
from bot.handlers import start, language, survey, vacancies, admin, manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot) -> None:
    """При старте устанавливаем вебхук"""
    await bot.set_webhook(
        url=f"{WEBHOOK_URL}{WEBHOOK_PATH}",
        drop_pending_updates=True
    )
    logger.info("✅ Webhook установлен")

async def on_shutdown(bot: Bot) -> None:
    """При остановке удаляем вебхук"""
    await bot.delete_webhook()
    logger.info("✅ Webhook удален")

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
    
    # Для Render используем вебхук
    from aiohttp import web
    
    app = web.Application()
    webhook_requests_handler = SimpleWebhookResponse(
        bot=bot,
        dispatcher=dp,
        path=WEBHOOK_PATH,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    app.on_startup.append(lambda _: on_startup(bot))
    app.on_shutdown.append(lambda _: on_shutdown(bot))
    
    logger.info(f"✅ Бот запущен на порту {WEBHOOK_PORT}")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=WEBHOOK_PORT)
    await site.start()
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")