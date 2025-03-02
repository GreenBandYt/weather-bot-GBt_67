from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    """Создает клавиатуру меню для команды /start."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("🌦️ Погода"),
                KeyboardButton("📊 Статистика"),
            ],
        ],
        resize_keyboard=True,  # Клавиатура уменьшается под размер кнопок
        one_time_keyboard=False  # Клавиатура не исчезает автоматически после нажатия
    )
    return keyboard

# Добавьте другие функции для создания клавиатур по мере необходимости