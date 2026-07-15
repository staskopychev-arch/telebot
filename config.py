"""Конфигурация бота — загрузка токенов и настроек из .env."""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ExchangeRate-API Key (https://www.exchangerate-api.com/)
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")

# Базовая валюта по умолчанию
DEFAULT_BASE_CURRENCY = "USD"

# Популярные валюты для быстрого доступа
POPULAR_CURRENCIES = {
    "USD": "🇺🇸 Доллар США",
    "EUR": "🇪🇺 Евро",
    "RUB": "🇷🇺 Рубль",
    "GBP": "🇬🇧 Фунт стерлингов",
    "UAH": "🇺🇦 Гривна",
    "CNY": "🇨🇳 Юань",
    "TRY": "🇹🇷 Турецкая лира",
}

# URL ExchangeRate API
EXCHANGE_API_URL = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
