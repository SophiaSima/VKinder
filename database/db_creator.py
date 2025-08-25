from database.db_models import Base
from sqlalchemy import create_engine
from config import DATABASE_URL


from database.db_models import Base
from config import DATABASE_URL


def create_database():
    """Создает все таблицы в базе данных"""
    # Создаем движок для подключения к БД
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True для отладки (показывает SQL-запросы)

    try:
        print("Создание таблиц в базе данных...")
        Base.metadata.create_all(engine)
        print("✅ Таблицы успешно созданы!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        return False


if __name__ == "__main__":
    create_database()