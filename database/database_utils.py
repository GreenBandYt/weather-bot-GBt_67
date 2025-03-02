import sqlite3
import configparser
from datetime import datetime

# Чтение конфигурации из config.ini
config = configparser.ConfigParser()
config.read('database/config.ini')
DATABASE_PATH = config['database']['path']

def create_connection():
    """Создает соединение с базой данных."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def log_query(user_id, query):
    """Логирует запрос пользователя."""
    conn = create_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (user_id, query, timestamp) VALUES (?, ?, ?)", (user_id, query, timestamp))
    conn.commit()
    conn.close()

def get_statistics():
    """Получает статистику из базы данных."""
    conn = create_connection()
    cursor = conn.cursor()

    # Общее количество запросов
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_requests = cursor.fetchone()[0]

    # Самые популярные города (предполагаем, что запросы начинаются с "Погода для " или "Пользователь выбрал город ")
    cursor.execute("SELECT query, COUNT(*) as count FROM logs WHERE query LIKE 'Погода для%' OR query LIKE 'Пользователь выбрал город %' GROUP BY query ORDER BY count DESC LIMIT 3")
    popular_queries = cursor.fetchall()

    # Количество запросов по пользователям
    cursor.execute("SELECT user_id, COUNT(*) as count FROM logs GROUP BY user_id ORDER BY count DESC")
    user_requests = cursor.fetchall()

    # Период запросов (самый ранний и самый поздний)
    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM logs")
    time_range = cursor.fetchone()

    conn.close()

    return {
        "total_requests": total_requests,
        "popular_queries": popular_queries,
        "user_requests": user_requests,
        "time_range": time_range
    }

def get_all_logs():
    """Получает все записи из таблицы logs."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, query, timestamp FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return logs