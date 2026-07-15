"""Сервис для работы с ExchangeRate-API."""

import aiohttp
from config import EXCHANGE_API_KEY, EXCHANGE_API_URL, POPULAR_CURRENCIES


class ExchangeService:
    """Асинхронный сервис получения курсов валют."""

    @staticmethod
    async def _fetch(base: str) -> dict | None:
        """Получить данные от API для базовой валюты."""
        url = EXCHANGE_API_URL.format(api_key=EXCHANGE_API_KEY, base=base.upper())
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 200:
                        return None
                    data = await resp.json()
                    if data.get("result") != "success":
                        return None
                    return data
        except (aiohttp.ClientError, TimeoutError):
            return None

    @staticmethod
    async def get_rate(base: str, target: str) -> float | None:
        """Получить курс одной валюты.

        Args:
            base: Код базовой валюты (напр. USD).
            target: Код целевой валюты (напр. EUR).

        Returns:
            Курс обмена или None при ошибке.
        """
        data = await ExchangeService._fetch(base)
        if data is None:
            return None
        rates = data.get("conversion_rates", {})
        return rates.get(target.upper())

    @staticmethod
    async def get_all_rates(base: str) -> dict | None:
        """Получить все курсы от базовой валюты.

        Returns:
            Словарь {код_валюты: курс} или None при ошибке.
        """
        data = await ExchangeService._fetch(base)
        if data is None:
            return None
        return data.get("conversion_rates")

    @staticmethod
    async def get_popular_rates(base: str) -> dict | None:
        """Получить курсы только популярных валют.

        Returns:
            Словарь {код_валюты: курс} только для POPULAR_CURRENCIES.
        """
        all_rates = await ExchangeService.get_all_rates(base)
        if all_rates is None:
            return None
        return {
            code: all_rates[code]
            for code in POPULAR_CURRENCIES
            if code in all_rates and code != base.upper()
        }

    @staticmethod
    async def convert(amount: float, from_cur: str, to_cur: str) -> float | None:
        """Конвертировать сумму из одной валюты в другую.

        Args:
            amount: Сумма для конвертации.
            from_cur: Исходная валюта.
            to_cur: Целевая валюта.

        Returns:
            Сконвертированная сумма или None при ошибке.
        """
        rate = await ExchangeService.get_rate(from_cur, to_cur)
        if rate is None:
            return None
        return round(amount * rate, 2)
