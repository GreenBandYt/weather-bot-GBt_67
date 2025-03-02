# dictionaries/text_actions.py

from handlers.user_handlers import (
    handle_start,
    handle_help
)

TEXT_ACTIONS = {

    # Действия для пользователя
    "🔔 Запустить бота": handle_start,
    "📊 Статистика": handle_help,

}
