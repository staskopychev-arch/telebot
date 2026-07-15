# 💱 Telegram-бот курсов валют

Бот для Telegram, который показывает актуальные курсы валют и выполняет конвертацию.

## 🚀 Быстрый старт

### 1. Создай бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot`
3. Введи имя и username для бота
4. Скопируй **токен**

### 2. Получи API-ключ

1. Зарегистрируйся на [ExchangeRate-API](https://www.exchangerate-api.com/)
2. Скопируй API-ключ из личного кабинета

### 3. Установи зависимости

```bash
cd telegram-bot
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 4. Настрой токены

Открой файл `.env` и замени placeholder'ы на реальные значения:

```
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
EXCHANGE_API_KEY=your_api_key_here
```

### 5. Запусти бота

```bash
python bot.py
```

## 📋 Команды

| Команда | Описание |
|---------|----------|
| `/start` | Главное меню с кнопками |
| `/help` | Справка по командам |
| `/rate EUR` | Курс EUR к USD |
| `/convert 100 USD RUB` | Конвертировать 100 USD в RUB |

## 🛠 Структура проекта

```
telegram-bot/
├── bot.py              # Точка входа
├── config.py           # Конфигурация
├── handlers/           # Обработчики команд
│   ├── start.py        # /start и /help
│   └── currency.py     # Курсы и конвертер
├── services/
│   └── exchange.py     # Сервис ExchangeRate API
├── keyboards/
│   └── currency_kb.py  # Inline-клавиатуры
├── .env                # Токены (не коммитить!)
└── requirements.txt    # Зависимости
```

## 📝 Лицензия

MIT
