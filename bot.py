"""Telegram-бот курсов валют — точка входа."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import start, currency


async def main() -> None:
    """Запуск бота."""
    # Проверка токена
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не задан! Укажи его в файле .env")
        sys.exit(1)

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Инициализация бота и диспетчера
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Подключение роутеров
    dp.include_router(start.router)
    dp.include_router(currency.router)

    # Запуск
    logger.info("🚀 Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
