# dictionaries/callback_actions.py

from handlers.user_handlers import (
    handle_get_weather,  # Исправлено
    handle_set_city,
    handle_details,
)

CALLBACK_ACTIONS = {
    "weather": handle_get_weather,  # Исправлено
    "set_city": handle_set_city,
    "details": handle_details,  # Добавляем обработчик для кнопки "Подробно"
}

