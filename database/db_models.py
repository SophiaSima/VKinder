from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Создаем базовый класс для моделей
Base = declarative_base()

class User(Base):
    """Модель пользователя бота (тот, кто ищет пару)"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Наш внутренний ID
    vk_id = Column(Integer, unique=True, nullable=False)       # ID пользователя ВКонтакте
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(Integer)  # 1 — женский, 2 — мужской
    city = Column(String)

    # Связи с другими таблицами
    searches = relationship("Search", back_populates="user")
    search_results = relationship("SearchResult", back_populates="user")


class Profile(Base):
    """Модель найденного профиля (кандидата)"""
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Наш внутренний ID
    vk_id = Column(Integer, unique=True, nullable=False)       # ID кандидата ВКонтакте
    first_name = Column(String)
    last_name = Column(String)
    profile_link = Column(String)  # Ссылка на профиль
    photos = Column(JSON)          # Список фото в формате JSON

    # Связи с другими таблицами
    search_results = relationship("SearchResult", back_populates="profile")


class Search(Base):
    """Модель поискового запроса (история поисков)"""
    __tablename__ = 'searches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    city = Column(String)
    age_from = Column(Integer)
    age_to = Column(Integer)
    gender = Column(Integer)  # 1 — женский, 2 — мужский
    search_date = Column(DateTime, default=datetime.now)

    # Связи с другими таблицами
    user = relationship("User", back_populates="searches")
    results = relationship("SearchResult", back_populates="search")


class SearchResult(Base):
    """Модель результатов поиска (связь поиска с профилями)"""
    __tablename__ = 'search_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    search_id = Column(Integer, ForeignKey('searches.id'), nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Кто искал
    viewed = Column(Boolean, default=False)  # Просмотрено ли
    liked = Column(Boolean, default=False)   # Добавлено в избранное

    # Связи с другими таблицами
    search = relationship("Search", back_populates="results")
    profile = relationship("Profile", back_populates="search_results")
    user = relationship("User", back_populates="search_results")