# handlers/message_handlers.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

from dictionaries.text_actions import TEXT_ACTIONS
from dictionaries.callback_actions import CALLBACK_ACTIONS  # Импортируем ваш словарь
from dictionaries.smart_replies import get_smart_reply
from dictionaries.states import STATE_HANDLERS
from handlers.user_handlers import get_user_state # Добавляем импорт

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("🛠️ Вызван универсальный обработчик handle_user_input")
    user_id = update.effective_user.id
    user_state = await get_user_state(user_id, context)  # Чтение из context.user_data

    # Проверяем состояние пользователя
    if user_state in STATE_HANDLERS:
        handler = STATE_HANDLERS[user_state]  # Получаем функцию напрямую
        try:
            if callable(handler):
                logging.info(f"🔍 Состояние пользователя {user_id}: {user_state}. Вызывается {handler.__name__}.")
                await handler(update, context)
                return
            else:
                raise ValueError(f"Обработчик для состояния {user_state} не является функцией.")
        except Exception as e:
            logging.error(f"❌ Ошибка в {handler.__name__} для состояния {user_state}: {e}")
            await update.message.reply_text("❌ Ошибка обработки. Обратитесь к администратору.")
            return

    # Если user_idle, проверяем текст
    user_text = update.message.text.strip()
    action = TEXT_ACTIONS.get(user_text)
    if action:
        logging.info(f"🔘 Действие для текста '{user_text}': {action.__name__}.")
        await action(update, context)
        return

    response = get_smart_reply(user_text)
    if response:
        logging.info(f"🤖 Умный ответ на '{user_text}': {response}.")
        await update.message.reply_text(response)
        return

    logging.info(f"❓ Пользователь {user_id} отправил непонятный текст: '{user_text}'.")
    await update.message.reply_text(
        "Извините, я вас не понял. Укажите город или используйте меню. 🤔"
    )

async def handle_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Универсальный обработчик для инлайн-кнопок.
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    logging.info(f"Получено callback_data: {callback_data}")

    # Поиск обработчика по callback_data
    action = CALLBACK_ACTIONS.get(callback_data)

    if action:
        try:
            await action(update, context)
        except Exception as e:
            logging.error(f"Ошибка при выполнении {action}: {e}")
            await query.edit_message_text(
                "Произошла ошибка при выполнении действия. Обратитесь к администратору."
            )
    else:
        logging.warning(f"Неизвестное callback_data: {callback_data}")
        await query.edit_message_text(
            "Кнопка больше не активна. Попробуйте снова или обратитесь к администратору."
        )