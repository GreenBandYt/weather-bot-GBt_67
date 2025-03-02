# dictionaries/callback_actions.py

from handlers.user_handlers import (
    handle_weather,
    handle_set_city,
    handle_statistic,

)

CALLBACK_ACTIONS = {
    "weather": handle_weather,
    "set_city": handle_set_city,
    "statistic": handle_statistic,

}
