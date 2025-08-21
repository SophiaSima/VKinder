# database/db_models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Создаем базовый класс для моделей
Base = declarative_base()

# Вспомогательная таблица для связи "многие-ко-многим" между User и Profile (Избранное)
favorites_table = Table(
    'favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.vk_id'), primary_key=True),
    Column('profile_id', Integer, ForeignKey('searched_profiles.vk_id'), primary_key=True)
)

# Вспомогательная таблица для учета показанных анкет
shown_profiles_table = Table(
    'shown_profiles', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.vk_id')),
    Column('profile_id', Integer, ForeignKey('searched_profiles.vk_id')),
    Column('shown_at', DateTime, default=datetime.now)
)

class User(Base):
    """Модель пользователя бота (тот, кто ищет пару)"""
    __tablename__ = 'users'

    vk_id = Column(Integer, primary_key=True)  # ID пользователя ВКонтакте
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(Integer)  # 1 — женский, 2 — мужской
    city = Column(String)

    # Связи с другими таблицами
    favorites = relationship("SearchedProfile", secondary=favorites_table, back_populates="favorited_by")
    shown_profiles = relationship("SearchedProfile", secondary=shown_profiles_table, back_populates="shown_to")

class SearchedProfile(Base):
    """Модель найденного профиля (кандидата)"""
    __tablename__ = 'searched_profiles'

    vk_id = Column(Integer, primary_key=True)  # ID кандидата ВКонтакте
    first_name = Column(String)
    last_name = Column(String)
    profile_link = Column(String)  # Ссылка на профиль

    # ID фотографий для attachment (в формате photo123456789_987654321)
    photo_1_id = Column(String)
    photo_2_id = Column(String)
    photo_3_id = Column(String)

    # Связи с другими таблицами
    favorited_by = relationship("User", secondary=favorites_table, back_populates="favorites")
    shown_to = relationship("User", secondary=shown_profiles_table, back_populates="shown_profiles")