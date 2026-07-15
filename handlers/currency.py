"""Обработчики курсов валют и конвертера."""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from config import POPULAR_CURRENCIES, DEFAULT_BASE_CURRENCY
from services.exchange import ExchangeService
from keyboards.currency_kb import (
    get_main_menu_kb,
    get_base_currency_kb,
    get_target_currency_kb,
    get_back_to_menu_kb,
    get_converter_amount_kb,
)

router = Router()


class ConverterState(StatesGroup):
    """FSM-состояния конвертера."""
    waiting_for_amount = State()


# ── Текстовые команды ────────────────────────────────────────────────


@router.message(Command("rate"))
async def cmd_rate(message: Message) -> None:
    """Быстрый курс валюты: /rate EUR."""
    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            "⚠️ Укажи код валюты!\nПример: <code>/rate EUR</code>",
            parse_mode="HTML",
        )
        return

    target = args[1].upper()
    base = DEFAULT_BASE_CURRENCY

    loading = await message.answer("⏳ Загружаю курс...")
    rate = await ExchangeService.get_rate(base, target)

    if rate is None:
        await loading.edit_text(
            f"❌ Не удалось получить курс <b>{target}</b>.\n"
            "Проверь код валюты и попробуй снова.",
            parse_mode="HTML",
            reply_markup=get_back_to_menu_kb(),
        )
        return

    flag = POPULAR_CURRENCIES.get(target, "").split()[0] if target in POPULAR_CURRENCIES else "💰"
    await loading.edit_text(
        f"{flag} <b>1 {base} = {rate:,.4f} {target}</b>",
        parse_mode="HTML",
        reply_markup=get_back_to_menu_kb(),
    )


@router.message(Command("convert"))
async def cmd_convert(message: Message) -> None:
    """Конвертация: /convert 100 USD RUB."""
    args = message.text.split()
    if len(args) < 4:
        await message.answer(
            "⚠️ Формат: <code>/convert СУММА ИЗ В</code>\n"
            "Пример: <code>/convert 100 USD RUB</code>",
            parse_mode="HTML",
        )
        return

    try:
        amount = float(args[1].replace(",", "."))
    except ValueError:
        await message.answer("⚠️ Некорректная сумма! Укажи число.")
        return

    from_cur = args[2].upper()
    to_cur = args[3].upper()

    loading = await message.answer("⏳ Конвертирую...")
    result = await ExchangeService.convert(amount, from_cur, to_cur)

    if result is None:
        await loading.edit_text(
            f"❌ Не удалось конвертировать <b>{from_cur}</b> → <b>{to_cur}</b>.\n"
            "Проверь коды валют и попробуй снова.",
            parse_mode="HTML",
            reply_markup=get_back_to_menu_kb(),
        )
        return

    rate = await ExchangeService.get_rate(from_cur, to_cur)
    rate_str = f"\n📊 Курс: 1 {from_cur} = {rate:,.4f} {to_cur}" if rate else ""

    await loading.edit_text(
        f"🔄 <b>{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}</b>"
        f"{rate_str}",
        parse_mode="HTML",
        reply_markup=get_back_to_menu_kb(),
    )


# ── Callback: главное меню ───────────────────────────────────────────


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Возврат в главное меню."""
    await state.clear()
    await callback.message.edit_text(
        "💱 <b>Бот курсов валют</b>\n\nВыбери действие:",
        parse_mode="HTML",
        reply_markup=get_main_menu_kb(),
    )
    await callback.answer()


# ── Callback: популярные курсы ───────────────────────────────────────


@router.callback_query(F.data == "popular_rates")
async def cb_popular_rates(callback: CallbackQuery) -> None:
    """Выбор базовой валюты для популярных курсов."""
    await callback.message.edit_text(
        "💱 <b>Популярные курсы</b>\n\nВыбери базовую валюту:",
        parse_mode="HTML",
        reply_markup=get_base_currency_kb("popular"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("popular_"))
async def cb_show_popular(callback: CallbackQuery) -> None:
    """Показать популярные курсы для выбранной базовой валюты."""
    base = callback.data.split("_", 1)[1]

    await callback.message.edit_text("⏳ Загружаю курсы...", parse_mode="HTML")
    rates = await ExchangeService.get_popular_rates(base)

    if rates is None:
        await callback.message.edit_text(
            "❌ Ошибка загрузки курсов. Попробуй позже.",
            reply_markup=get_back_to_menu_kb(),
        )
        await callback.answer()
        return

    base_flag = POPULAR_CURRENCIES.get(base, "💰").split()[0]
    lines = [f"📊 <b>Курсы от {base_flag} {base}:</b>\n"]

    for code, rate in rates.items():
        flag = POPULAR_CURRENCIES.get(code, "💰").split()[0]
        lines.append(f"  {flag} <b>{code}</b>: {rate:,.4f}")

    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=get_back_to_menu_kb(),
    )
    await callback.answer()


# ── Callback: все валюты ─────────────────────────────────────────────


@router.callback_query(F.data == "all_currencies")
async def cb_all_currencies(callback: CallbackQuery) -> None:
    """Показать список всех доступных валют."""
    await callback.message.edit_text("⏳ Загружаю список валют...")
    rates = await ExchangeService.get_all_rates(DEFAULT_BASE_CURRENCY)

    if rates is None:
        await callback.message.edit_text(
            "❌ Ошибка загрузки. Попробуй позже.",
            reply_markup=get_back_to_menu_kb(),
        )
        await callback.answer()
        return

    # Показываем только коды валют, сгруппированные
    codes = sorted(rates.keys())
    chunks = [codes[i : i + 10] for i in range(0, len(codes), 10)]
    lines = [f"📋 <b>Доступные валюты ({len(codes)} шт.):</b>\n"]

    for chunk in chunks[:6]:  # Показываем первые 60, чтобы не перегружать
        lines.append("  " + " • ".join(chunk))

    if len(chunks) > 6:
        remaining = len(codes) - 60
        lines.append(f"\n  ...и ещё {remaining} валют")

    lines.append(
        "\n💡 Используй <code>/rate КОД</code> для любой валюты"
    )

    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=get_back_to_menu_kb(),
    )
    await callback.answer()


# ── Callback: конвертер ──────────────────────────────────────────────


@router.callback_query(F.data == "converter_start")
async def cb_converter_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Начать конвертацию — выбор исходной валюты."""
    await state.clear()
    await callback.message.edit_text(
        "🔄 <b>Конвертер валют</b>\n\nВыбери исходную валюту:",
        parse_mode="HTML",
        reply_markup=get_base_currency_kb("convert_from"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("convert_from_"))
async def cb_convert_from(callback: CallbackQuery) -> None:
    """Выбрана исходная валюта — выбрать целевую."""
    base = callback.data.split("_")[-1]

    await callback.message.edit_text(
        f"🔄 <b>Конвертер</b>\n\n"
        f"Из: <b>{base}</b>\n"
        f"Выбери целевую валюту:",
        parse_mode="HTML",
        reply_markup=get_target_currency_kb(base),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("convert_to_"))
async def cb_convert_to(callback: CallbackQuery, state: FSMContext) -> None:
    """Выбрана целевая валюта — показать кнопки сумм."""
    parts = callback.data.split("_")
    base = parts[2]
    target = parts[3]

    # Сохраняем валюты в FSM и ждём ввод суммы
    await state.set_state(ConverterState.waiting_for_amount)
    await state.update_data(from_cur=base, to_cur=target)

    await callback.message.edit_text(
        f"🔄 <b>Конвертер</b>\n\n"
        f"Из: <b>{base}</b> → В: <b>{target}</b>\n\n"
        f"Выбери сумму или отправь число в чат:",
        parse_mode="HTML",
        reply_markup=get_converter_amount_kb(base, target),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("conv_"))
async def cb_convert_execute(callback: CallbackQuery) -> None:
    """Выполнить конвертацию с выбранной суммой."""
    parts = callback.data.split("_")
    amount = float(parts[1])
    from_cur = parts[2]
    to_cur = parts[3]

    await callback.message.edit_text("⏳ Конвертирую...", parse_mode="HTML")
    result = await ExchangeService.convert(amount, from_cur, to_cur)

    if result is None:
        await callback.message.edit_text(
            "❌ Ошибка конвертации. Попробуй позже.",
            reply_markup=get_back_to_menu_kb(),
        )
        await callback.answer()
        return

    rate = await ExchangeService.get_rate(from_cur, to_cur)
    rate_str = f"\n📊 Курс: 1 {from_cur} = {rate:,.4f} {to_cur}" if rate else ""

    await callback.message.edit_text(
        f"✅ <b>{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}</b>"
        f"{rate_str}",
        parse_mode="HTML",
        reply_markup=get_back_to_menu_kb(),
    )
    await callback.answer()


# ── Ввод суммы текстом ───────────────────────────────────────────────


@router.message(ConverterState.waiting_for_amount)
async def msg_convert_amount(message: Message, state: FSMContext) -> None:
    """Пользователь отправил число для конвертации."""
    text = message.text.strip().replace(",", ".")

    try:
        amount = float(text)
    except ValueError:
        await message.answer(
            "⚠️ Отправь число для конвертации.\n"
            "Например: <code>150</code> или <code>99.5</code>",
            parse_mode="HTML",
        )
        return

    data = await state.get_data()
    from_cur = data["from_cur"]
    to_cur = data["to_cur"]

    # Сбрасываем состояние
    await state.clear()

    loading = await message.answer("⏳ Конвертирую...")
    result = await ExchangeService.convert(amount, from_cur, to_cur)

    if result is None:
        await loading.edit_text(
            f"❌ Ошибка конвертации <b>{from_cur}</b> → <b>{to_cur}</b>.",
            parse_mode="HTML",
            reply_markup=get_back_to_menu_kb(),
        )
        return

    rate = await ExchangeService.get_rate(from_cur, to_cur)
    rate_str = f"\n📊 Курс: 1 {from_cur} = {rate:,.4f} {to_cur}" if rate else ""

    await loading.edit_text(
        f"✅ <b>{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}</b>"
        f"{rate_str}",
        parse_mode="HTML",
        reply_markup=get_back_to_menu_kb(),
    )
