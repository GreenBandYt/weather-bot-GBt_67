import httpx
from datetime import datetime
import logging  # Добавляем импорт logging

from utils.keyboards import get_start_keyboard  # Оставляем импорт, даже если не используется, на случай будущих изменений
from telegram import Update
from telegram.ext import ContextTypes
from config import GBt_key

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from database.database_utils import log_query, get_statistics, get_all_logs  # Убедимся, что импортируем все функции корректно

# Настройка логирования (если нужно, можно перенести в отдельный файл или использовать глобальную настройку)
logging.basicConfig(level=logging.INFO)

async def handle_get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает кнопку KeyboardButton("️ Погода")."""
    user_id = update.effective_user.id
    city = context.user_data.get(f"city_{user_id}", 'Smolensk')
    weather_data = await get_weather(city)

    # Создаем инлайн-клавиатуру с двумя кнопками (без "Подробно")
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Погода", callback_data="weather")],
        [InlineKeyboardButton(text="Установить город", callback_data="set_city")]
    ])

    if isinstance(weather_data, dict):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"🌆 Город: {weather_data['city_name']}\n"
                                            f"🕒 Текущее время: {weather_data['current_time']}\n"  # Добавлено текущее время
                                            f"🌡️ Температура: {weather_data['temperature']}°C\n"
                                            f"🤗 Ощущается как: {weather_data['feels_like']}°C\n"
                                            f"☁️ Погодные условия: {weather_data['description']}\n"
                                            f"💨 Скорость ветра: {weather_data['wind_speed']} м/с ({weather_data['wind_speed_kmh']} км/ч)\n"
                                            f"💧 Влажность: {weather_data['humidity']}%\n"
                                            f"🔽 Давление: {weather_data['pressure']} мм рт. ст.\n"
                                            f"🌅 Восход солнца: {weather_data['sunrise']}\n"
                                            f"🌇 Закат солнца: {weather_data['sunset']}",
                                       reply_markup=inline_keyboard)  # Добавляем инлайн-клавиатуру
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=weather_data, reply_markup=inline_keyboard)  # Добавляем инлайн-клавиатуру

    # Логируем запрос погоды
    log_query(user_id, f"Погода для {city}")
    logging.info(f"Пользователь {user_id} запросил погоду для города {city}")

    # ПРИМЕЧАНИЕ: Клавиатура может исчезнуть после инлайн-кнопок, если пользователь или Telegram её скроют,
    # так как мы не отправляем сообщение для её восстановления. Это соответствует твоему требованию
    # не выводить никакой текст.

async def handle_statistic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает кнопку KeyboardButton(" Статистика")."""
    stats = get_statistics()

    # Формируем ответ с данными
    response = "📊 Статистика запросов:\n\n"
    response += f"Общее количество запросов: {stats['total_requests']}\n\n"
    response += "Топ-3 популярных запросов:\n"
    for query, count in stats['popular_queries']:
        city_name = query.replace("Погода для ", "").replace("Пользователь выбрал город '", "").replace("'", "")
        response += f"- {city_name}: {count} раз\n"
    response += "\nЗапросы по пользователям:\n"
    for user_id, count in stats['user_requests']:
        response += f"- Пользователь {user_id}: {count} запросов\n"
    response += f"\nПериод запросов: с {stats['time_range'][0]} по {stats['time_range'][1] if stats['time_range'][1] else 'нет данных'}"

    # Создаем инлайн-кнопку "Подробно" под сообщением
    details_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Подробно", callback_data="details")]
    ])

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=details_keyboard)

async def handle_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает инлайн-кнопку 'Подробно' и выводит каждую запись из логов как отдельную карточку."""
    logs = get_all_logs()

    if not logs:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Нет записей в логе.")
        return

    # Отправляем каждую запись как отдельное сообщение (карточку)
    for log in logs:
        user_id, query, timestamp = log
        card = f"📰 Запрос #{len(logs) - logs.index(log)}:\n"
        card += f"👤 ID пользователя: {user_id}\n"
        card += f"📜 Запрос: {query}\n"
        card += f"🕒 Время: {timestamp}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=card)

from datetime import datetime, timedelta

async def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={GBt_key}&units=metric&lang=ru'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=20)
            if response.status_code == 200:
                data = response.json()
                city_name = data['name']
                temperature = data['main']['temp']
                feels_like = data['main']['feels_like']
                description = data['weather'][0]['description']
                wind_speed = data['wind']['speed']
                wind_speed_kmh = round(wind_speed * 3.6, 1)
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                pressure_mmHg = round(pressure * 0.75006)
                sunrise = data['sys']['sunrise']
                sunset = data['sys']['sunset']
                dt = data['dt']  # Текущая временная метка от API (в UTC)
                timezone = data['timezone']  # Смещение часового пояса в секундах

                # Вычисляем текущее время в городе
                current_time_utc = datetime.utcfromtimestamp(dt)  # Преобразуем dt в UTC
                current_time_local = current_time_utc + timedelta(seconds=timezone)  # Добавляем смещение
                current_time = current_time_local.strftime('%H:%M:%S')

                # Преобразуем время восхода и заката с учетом часового пояса
                sunrise_time = (datetime.utcfromtimestamp(sunrise) + timedelta(seconds=timezone)).strftime('%H:%M:%S')
                sunset_time = (datetime.utcfromtimestamp(sunset) + timedelta(seconds=timezone)).strftime('%H:%M:%S')

                return {
                    "city_name": city_name,
                    "temperature": temperature,
                    "feels_like": feels_like,
                    "description": description,
                    "wind_speed": wind_speed,
                    "wind_speed_kmh": wind_speed_kmh,
                    "humidity": humidity,
                    "pressure": pressure_mmHg,
                    "sunrise": sunrise_time,
                    "sunset": sunset_time,
                    "current_time": current_time  # Добавлено текущее время
                }
            else:
                return f"Ошибка: не удалось получить данные о погоде для {city} (код {response.status_code})"
    except httpx.ReadTimeout:
        return "Превышено время ожидания ответа от сервера. Попробуйте позже."
    except httpx.RequestError as e:
        return f"Произошла ошибка при запросе данных: {e}"

async def handle_set_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает инлайн-кнопку 'Установить город'."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите название города:"
    )
    await set_user_state(update.effective_user.id, "STATE_WAITING_FOR_CITY", context)  # Добавлен context

async def process_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает ввод города от пользователя."""
    user_id = update.effective_user.id
    city = update.message.text.strip()

    # Логируем факт выбора города
    log_query(user_id, f"Пользователь выбрал город '{city}'")

    # Сохраняем город в user_data
    context.user_data[f'city_{user_id}'] = city

    # Сбрасываем состояние пользователя
    await set_user_state(user_id, "user_idle", context)

    # Подтверждаем установку города
    await update.message.reply_text(f"Город успешно установлен: {city} ")

    # Запрашиваем и выводим погоду автоматически после установки города
    weather_data = await get_weather(city)
    if isinstance(weather_data, dict):
        response = (f"🌆 Город: {weather_data['city_name']}\n"
                    f"🕒 Текущее время: {weather_data['current_time']}\n"  # Добавлено текущее время
                    f"🌡️ Температура: {weather_data['temperature']}°C\n"
                    f"🤗 Ощущается как: {weather_data['feels_like']}°C\n"
                    f"☁️ Погодные условия: {weather_data['description']}\n"
                    f"💨 Скорость ветра: {weather_data['wind_speed']} м/с ({weather_data['wind_speed_kmh']} км/ч)\n"
                    f"💧 Влажность: {weather_data['humidity']}%\n"
                    f"🔽 Давление: {weather_data['pressure']} мм рт. ст.\n"
                    f"🌅 Восход солнца: {weather_data['sunrise']}\n"
                    f"🌇 Закат солнца: {weather_data['sunset']}")
    else:
        response = weather_data

    # Создаем ту же инлайн-клавиатуру, что и в handle_get_weather (без "Подробно")
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Погода", callback_data="weather")],
        [InlineKeyboardButton(text="Установить город", callback_data="set_city")]
    ])

    await update.message.reply_text(response, reply_markup=inline_keyboard)  # Используем инлайн-кнопки

    # ПРИМЕЧАНИЕ: Клавиатура может исчезнуть после инлайн-кнопок, если пользователь или Telegram её скроют,
    # так как мы не отправляем сообщение для её восстановления. Это соответствует твоему требованию
    # не выводить никакой текст.

    # Логируем запрос погоды
    log_query(user_id, f"Погода для {city}")
    logging.info(f"Пользователь {user_id} запросил погоду для города {city}")

async def get_user_state(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получает текущее состояние пользователя."""
    return context.user_data.get(f"state_{user_id}", "user_idle")

async def set_user_state(user_id: int, state: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает состояние пользователя."""
    context.user_data[f"state_{user_id}"] = state