# utils/keyboards.py

from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    """Создает клавиатуру меню для команды /start."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(" Запустить бота"),
                KeyboardButton(" Статистика"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard

# Добавьте другие функции для создания клавиатур по мере необходимости