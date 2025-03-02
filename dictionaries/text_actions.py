# dictionaries/text_actions.py

from handlers.user_handlers import (
    handle_get_weather,
    handle_statistic
)

TEXT_ACTIONS = {

    # Действия для пользователя
    "🌦️ Погода": handle_get_weather,
    "📊 Статистика": handle_statistic,

}
