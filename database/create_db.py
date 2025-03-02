# database/create_db.py

import sqlite3
import configparser

# Чтение конфигурации из config.ini
config = configparser.ConfigParser()
config.read('database/config.ini')
DATABASE_PATH = config['database']['path']

def create_connection():
    """Создает соединение с базой данных."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def create_table():
    """Создает таблицу для хранения логов."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("База данных и таблица 'logs' созданы.")