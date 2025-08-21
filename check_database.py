# check_database.py
import sqlite3
import os
from sqlalchemy import create_engine, inspect
from config import DATABASE_URL


def check_db_structure():
    print("=== ПРОВЕРКА СТРУКТУРЫ БАЗЫ ДАННЫХ ===\n")

    # Создаем движок для проверки
    engine = create_engine(DATABASE_URL)

    # Проверяем существование файла
    db_path = 'database.db'
    print(f"Файл БД существует: {os.path.exists(db_path)}")

    if os.path.exists(db_path):
        print(f"Размер файла: {os.path.getsize(db_path)} байт")
    else:
        print("❌ Файл database.db не найден!")
        return False

    print("\n" + "=" * 50 + "\n")

    try:
        # Проверяем через SQLite
        print("1. Проверка через SQLite:")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("   Таблицы в базе данных:")
        for table in tables:
            print(f"     - {table[0]}")

        # Проверяем структуру каждой таблицы
        for table_name in [table[0] for table in tables]:
            print(f"\n   Структура таблицы '{table_name}':")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                print(f"     - {col[1]} ({col[2]})")

        conn.close()

        print("\n" + "=" * 50 + "\n")

        # Проверяем через SQLAlchemy
        print("2. Проверка через SQLAlchemy:")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("   Таблицы:", tables)

        return True

    except Exception as e:
        print(f"❌ Ошибка при проверке БД: {e}")
        return False


if __name__ == "__main__":
    success = check_db_structure()
    if success:
        print("\n✅ База данных в порядке!")
    else:
        print("\n❌ Проблемы с базой данных!")