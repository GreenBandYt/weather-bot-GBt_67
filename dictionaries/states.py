# dictionaries/states.py


from handlers.user_handlers import process_city_input

# Словарь обработчиков состояний
STATE_HANDLERS = {
    "STATE_WAITING_FOR_CITY": process_city_input,  # Исправлено
}