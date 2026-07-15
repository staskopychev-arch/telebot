"""Inline-клавиатуры для бота."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import POPULAR_CURRENCIES


def get_main_menu_kb() -> InlineKeyboardMarkup:
    """Главное меню бота."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💱 Популярные курсы", callback_data="popular_rates"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Конвертер валют", callback_data="converter_start"),
    )
    builder.row(
        InlineKeyboardButton(text="📋 Все валюты", callback_data="all_currencies"),
    )
    return builder.as_markup()


def get_base_currency_kb(action: str = "popular") -> InlineKeyboardMarkup:
    """Клавиатура выбора базовой валюты.

    Args:
        action: Префикс для callback_data ('popular' или 'convert_from').
    """
    builder = InlineKeyboardBuilder()
    for code, name in POPULAR_CURRENCIES.items():
        builder.button(
            text=f"{name.split()[0]} {code}",
            callback_data=f"{action}_{code}",
        )
    builder.adjust(2)  # 2 кнопки в ряд
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"),
    )
    return builder.as_markup()


def get_target_currency_kb(base: str) -> InlineKeyboardMarkup:
    """Клавиатура выбора целевой валюты для конвертации.

    Args:
        base: Код базовой валюты (будет исключена из списка).
    """
    builder = InlineKeyboardBuilder()
    for code, name in POPULAR_CURRENCIES.items():
        if code != base:
            builder.button(
                text=f"{name.split()[0]} {code}",
                callback_data=f"convert_to_{base}_{code}",
            )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="converter_start"),
    )
    return builder.as_markup()


def get_back_to_menu_kb() -> InlineKeyboardMarkup:
    """Кнопка «Назад в меню»."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ В главное меню", callback_data="main_menu"),
    )
    return builder.as_markup()


def get_converter_amount_kb(base: str, target: str) -> InlineKeyboardMarkup:
    """Кнопки быстрого выбора суммы для конвертации."""
    builder = InlineKeyboardBuilder()
    for amount in [1, 10, 100, 1000, 5000]:
        builder.button(
            text=f"{amount} {base}",
            callback_data=f"conv_{amount}_{base}_{target}",
        )
    builder.adjust(3)
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="converter_start"),
    )
    return builder.as_markup()
