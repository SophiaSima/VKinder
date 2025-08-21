# database/db_creator.py
from database.db_models import Base
from sqlalchemy import create_engine
from config import DATABASE_URL

# Создаем движок для подключения к БД
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для отладки (показывает SQL-запросы)

# Создаем все таблицы в базе данных
if __name__ == "__main__":
    print("Создание таблиц в базе данных...")
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы!")