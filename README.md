# 🌦️ Telegram Weather Bot - GBt_67

Этот бот для Telegram позволяет пользователям получать подробную информацию о погоде в любом городе мира. После отправки названия города бот запрашивает данные через API OpenWeatherMap и отправляет пользователю актуальную информацию о погоде, включая температуру, влажность, давление, скорость ветра, условия, время восхода и заката, а также текущее время в городе.

📌 **Функционал:**  
- Получение погоды для любых городов мира (без ограничений).  
- Использование инлайн-кнопок и кнопок меню для удобного управления ботом.  
- Логирование всех запросов пользователей (ID пользователя, запрос, время запроса) в базу данных SQLite.  
- Вывод статистики запросов в виде читаемого текстового формата.  
- Подробный просмотр всех запросов в виде отдельных карточек с ID пользователя, запросом и временем через инлайн-кнопку "Подробно".  
- Автоматическое восстановление клавиатуры меню ("Погода", "Статистика") без вывода лишнего текста или пустых строк.  

## 🚀 **Как запустить бота?**  

### 1️⃣ Клонируйте репозиторий  
```bash
git clone https://github.com/ТВОЙ_GITHUB/weather-bot-GBt_67.git
cd weather-bot-GBt_67
```

### 2️⃣ Установите зависимости  
```bash
pip install -r requirements.txt
```

### 3️⃣ Создайте файл `config.py`  
Добавьте в него API-ключи:  
```python
TOKEN = "ТВОЙ_ТЕЛЕГРАМ_API_ТОКЕН"
GBt_key = "ТВОЙ_OPENWEATHERMAP_API_КЛЮЧ"
```

**Важно!**  
Файл `config.py` не загружается в репозиторий благодаря `.gitignore`.  

### 4️⃣ Запустите бота  
```bash
python bot.py
```

## 🛠 **Структура проекта**  

```
weather-bot-GBt_67/
│── bot.py                  # Основной код бота
│── config.py               # Конфигурационный файл с API-ключами (не коммитится)
│── requirements.txt        # Список зависимостей
│── .gitignore              # Исключенные файлы (config.py, базы данных и др.)
│── README.md               # Описание проекта
│── database/
│   ├── __init__.py         # Инициализация модуля database
│   ├── config.ini          # Конфигурация базы данных (например, путь к SQLite)
│   ├── create_db.py        # Создание базы данных и таблиц
│   └── database_utils.py   # Работа с SQLite (логирование запросов, статистика, подробные данные)
│── dictionaries/
│   ├── __init__.py         # Инициализация модуля dictionaries
│   ├── callback_actions.py # Действия для инлайн-кнопок
│   ├── smart_replies.py    # Умные ответы
│   ├── states.py           # Состояния пользователя
│   └── text_actions.py     # Действия для текстовых команд
│── handlers/
│   ├── __init__.py         # Инициализация модуля handlers
│   ├── message_handlers.py # Универсальный обработчик текстовых и инлайн-команд
│   └── user_handlers.py    # Обработчики пользовательских запросов (погода, статистика, детали)
│── utils/
│   ├── __init__.py         # Инициализация модуля utils
│   └── keyboards.py        # Создание клавиатур (меню и инлайн-кнопки)
```

## 📝 **Пример использования**  

1. **Запустите бота** с помощью команды `/start`.  
2. **Выберите действие** через меню: нажмите "🌦️ Погода" для получения погоды по умолчанию (Смоленск) или "Установить город" для ввода нового города.  
3. Введите название города (например, "Москва"), и бот отправит подробную информацию о погоде.  
4. Нажмите "📊 Статистика", чтобы увидеть общую статистику запросов (количество, популярные города, пользователи, период).  
5. Нажмите инлайн-кнопку "Подробно" под статистикой, чтобы увидеть все запросы в виде отдельных карточек с ID пользователя, запросом и временем.  
6. Все ваши действия автоматически логируются в базе данных SQLite.  

## 📊 **Статистика и подробности**  

- **Статистика**: При нажатии "📊 Статистика" бот выводит:  
  - Общее количество запросов.  
  - Топ-3 популярных городов (по запросам погоды и смене города).  
  - Количество запросов по каждому пользователю.  
  - Период запросов (от первой до последней записи).  
  - Под сообщением появляется инлайн-кнопка "Подробно".  

- **Подробности**: При нажатии "Подробно" каждая запись из логов выводится как отдельная карточка:  
  ```
  📰 Запрос #N:
  👤 ID пользователя: <user_id>
  📜 Запрос: <query>
  🕒 Время: <timestamp>
  ```
  Карточки отправляются по одной, что позволяет просматривать все запросы без ограничений длины сообщения.

---
