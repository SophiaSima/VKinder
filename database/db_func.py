# database/db_func.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import sys
sys.path.append('../VKinder')
sys.path.append('../VKinder/database')
sys.path.append('../VKinder/vk_tools')
from config import DATABASE_URL
from db_models import User, SearchedProfile, favorites_table, shown_profiles_table
from vk_api_func import get_top_photos

# Создаем движок и сессию для работы с БД
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def get_or_create_user(vk_id, first_name, last_name, age, gender, city):
    """Получает пользователя из БД или создает нового"""
    user = session.query(User).filter(User.vk_id == vk_id).first()

    if not user:
        user = User(
            vk_id=vk_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            city=city
        )
        session.add(user)
        session.commit()
        print(f"Создан новый пользователь: {first_name} {last_name}")
    else:
        print(f"Найден существующий пользователь: {first_name} {last_name}")

    return user


def add_searched_profile(profile_data, photos):
    """Добавляет найденный профиль в БД"""
    profile = session.query(SearchedProfile).filter(SearchedProfile.vk_id == profile_data['vk_id']).first()

    if not profile:
        profile = SearchedProfile(
            vk_id=profile_data['vk_id'],
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            profile_link=profile_data['profile_link'],
            photo_1_id=photos[0] if len(photos) > 0 else None,
            photo_2_id=photos[1] if len(photos) > 1 else None,
            photo_3_id=photos[2] if len(photos) > 2 else None
        )
        session.add(profile)
        session.commit()
        print(f"Добавлен новый профиль: {profile_data['first_name']} {profile_data['last_name']}")
    else:
        print(f"Профиль уже существует: {profile_data['first_name']} {profile_data['last_name']}")

    return profile


def mark_profile_as_shown(user_id, profile_id):
    """Помечает профиль как показанный пользователю"""
    # Проверяем, не показывали ли уже
    existing = session.query(shown_profiles_table).filter(
        shown_profiles_table.c.user_id == user_id,
        shown_profiles_table.c.profile_id == profile_id
    ).first()

    if not existing:
        # Добавляем запись о показе
        insert_stmt = shown_profiles_table.insert().values(
            user_id=user_id,
            profile_id=profile_id,
            shown_at=datetime.now()
        )
        session.execute(insert_stmt)
        session.commit()
        print(f"Профиль {profile_id} отмечен как показанный пользователю {user_id}")


def add_to_favorites(user_id, profile_id):
    """Добавляет профиль в избранное пользователя"""
    # Проверяем, не добавлен ли уже
    existing = session.query(favorites_table).filter(
        favorites_table.c.user_id == user_id,
        favorites_table.c.profile_id == profile_id
    ).first()

    if not existing:
        # Добавляем в избранное
        insert_stmt = favorites_table.insert().values(
            user_id=user_id,
            profile_id=profile_id
        )
        session.execute(insert_stmt)
        session.commit()
        print(f"Профиль {profile_id} добавлен в избранное пользователю {user_id}")
        return True
    else:
        print(f"Профиль {profile_id} уже в избранном у пользователя {user_id}")
        return False


def get_favorites(user_id):
    """Получает список избранных профилей пользователя"""
    user = session.query(User).filter(User.vk_id == user_id).first()
    if user:
        return user.favorites
    return []


def get_shown_profiles(user_id):
    """Получает список показанных профилей пользователю"""
    user = session.query(User).filter(User.vk_id == user_id).first()
    if user:
        return user.shown_profiles
    return []


# Закрываем сессию при завершении
def close_session():
    session.close()