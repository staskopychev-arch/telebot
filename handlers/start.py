"""Обработчики команд /start и /help."""

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.currency_kb import get_main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Приветствие и главное меню."""
    await message.answer(
        "👋 <b>Привет!</b>\n\n"
        "Я бот курсов валют 💱\n"
        "Могу показать актуальные курсы и конвертировать валюты.\n\n"
        "📌 <b>Быстрые команды:</b>\n"
        "• <code>/rate EUR</code> — курс EUR к USD\n"
        "• <code>/convert 100 USD RUB</code> — конвертировать\n\n"
        "Или используй кнопки ниже 👇",
        parse_mode="HTML",
        reply_markup=get_main_menu_kb(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Справка по командам."""
    await message.answer(
        "📖 <b>Доступные команды:</b>\n\n"
        "🔹 /start — Главное меню\n"
        "🔹 /help — Эта справка\n"
        "🔹 /rate <code>КОД</code> — Курс валюты к USD\n"
        "   Пример: <code>/rate EUR</code>\n"
        "🔹 /convert <code>СУММА ИЗ В</code> — Конвертация\n"
        "   Пример: <code>/convert 100 USD RUB</code>\n\n"
        "💡 Также можно использовать inline-кнопки в меню!",
        parse_mode="HTML",
        reply_markup=get_main_menu_kb(),
    )
