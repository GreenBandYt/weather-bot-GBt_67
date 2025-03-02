import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler # Добавляем импорт
from telegram import Update
from telegram.ext import ContextTypes

from handlers.message_handlers import handle_user_input, handle_inline_buttons # Добавляем импорт handle_inline_buttons
from handlers.user_handlers import set_user_state
from utils.keyboards import get_start_keyboard
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет клавиатуру меню после команды /start и устанавливает состояние user_idle."""
    keyboard = get_start_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот, который показывает погоду в любом городе. Напишите название города и я сообщу вам текущую погоду. Все ваши запросы логируются.",
        reply_markup=keyboard
    )
    # Устанавливаем начальное состояние user_idle
    await set_user_state(update.effective_user.id, "user_idle", context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input)
    app.add_handler(message_handler)

    # Добавляем обработчик инлайн-кнопок
    app.add_handler(CallbackQueryHandler(handle_inline_buttons))

    app.run_polling()