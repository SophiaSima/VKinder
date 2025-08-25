from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URL
from database.db_models import User, Profile, Search, SearchResult
from datetime import datetime
import json

# Создаем движок и фабрику сессий
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_or_create_user(vk_id, first_name, last_name, age, gender, city):
    """Получает пользователя из БД или создает нового"""
    session = Session()
    try:
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
            session.refresh(user)  # Обновляем объект после коммита
            print(f"✅ Создан новый пользователь: {first_name} {last_name}")
        else:
            print(f"✅ Найден существующий пользователь: {first_name} {last_name}")

        return user

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Ошибка при работе с пользователем: {e}")
        return None
    finally:
        session.close()


def get_or_create_profile(profile_data, photos):
    """Получает профиль из БД или создает новый"""
    session = Session()
    try:
        profile = session.query(Profile).filter(Profile.vk_id == profile_data['vk_id']).first()

        if not profile:
            profile = Profile(
                vk_id=profile_data['vk_id'],
                first_name=profile_data['first_name'],
                last_name=profile_data['last_name'],
                profile_link=profile_data['profile_link'],
                photos=json.dumps(photos)
            )
            session.add(profile)
            session.commit()
            session.refresh(profile)  # Обновляем объект после коммита
            print(f"✅ Добавлен новый профиль: {profile_data['first_name']} {profile_data['last_name']}")
        else:
            print(f"✅ Профиль уже существует: {profile_data['first_name']} {profile_data['last_name']}")

        return profile

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Ошибка при работе с профилем: {e}")
        return None
    finally:
        session.close()


def create_search(user_id, city, age_from, age_to, gender):
    """Создает новую запись поиска"""
    session = Session()
    try:
        search = Search(
            user_id=user_id,
            city=city,
            age_from=age_from,
            age_to=age_to,
            gender=gender,
            search_date=datetime.now()
        )
        session.add(search)
        session.commit()
        session.refresh(search)  # Обновляем объект после коммита
        print(f"✅ Создан новый поиск для пользователя {user_id}")
        return search

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Ошибка при создании поиска: {e}")
        return None
    finally:
        session.close()


def add_search_result(search_id, profile_id, user_id):
    """Добавляет результат поиска"""
    session = Session()
    try:
        existing = session.query(SearchResult).filter(
            and_(
                SearchResult.search_id == search_id,
                SearchResult.profile_id == profile_id
            )
        ).first()

        if not existing:
            search_result = SearchResult(
                search_id=search_id,
                profile_id=profile_id,
                user_id=user_id,
                viewed=False,
                liked=False
            )
            session.add(search_result)
            session.commit()
            print(f"✅ Добавлен результат поиска: search_id={search_id}, profile_id={profile_id}")
            return True
        else:
            print(f"⚠️ Результат поиска уже существует: search_id={search_id}, profile_id={profile_id}")
            return False

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Ошибка при добавлении результата поиска: {e}")
        return False
    finally:
        session.close()


def mark_profile_as_viewed(user_id, profile_id):
    """Помечает профиль как просмотренный"""
    session = Session()
    try:
        search_result = session.query(SearchResult).filter(
            and_(
                SearchResult.user_id == user_id,
                SearchResult.profile_id == profile_id
            )
        ).first()

        if search_result:
            search_result.viewed = True
            session.commit()
            print(f"✅ Профиль {profile_id} отмечен как просмотренный для пользователя {user_id}")
            return True
        else:
            print(f"❌ Результат поиска не найден для пользователя {user_id} и профиля {profile_id}")
            return False

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Ошибка при отметке просмотра: {e}")
        return False
    finally:
        session.close()


def add_to_favorites(user_id, profile_id):
    """Добавляет профиль в избранное"""
    session = Session()
    try:
        search_result = session.query(SearchResult).filter(
            and_(
                SearchResult.user_id == user_id,
                SearchResult.profile_id == profile_id
            )
        ).first()

        if search_result:
            search_result.liked = True
            session.commit()
            print(f"✅ Профиль {profile_id} добавлен в избранное пользователю {user_id}")
            return True
        else:
            print(f"❌ Результат поиска не найден для добавления в избранное")
            return False

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Ошибка при добавлении в избранное: {e}")
        return False
    finally:
        session.close()


def get_favorites(user_id):
    """Получает список избранных профилей пользователя"""
    session = Session()
    try:
        favorites = session.query(Profile).join(SearchResult).filter(
            and_(
                SearchResult.user_id == user_id,
                SearchResult.liked == True
            )
        ).all()

        print(f"✅ Найдено {len(favorites)} избранных профилей для пользователя {user_id}")
        return favorites

    except SQLAlchemyError as e:
        print(f"❌ Ошибка при получении избранного: {e}")
        return []
    finally:
        session.close()


def get_unviewed_profiles(user_id, search_id):
    """Получает непросмотренные профили для данного поиска"""
    session = Session()
    try:
        unviewed = session.query(Profile).join(SearchResult).filter(
            and_(
                SearchResult.user_id == user_id,
                SearchResult.search_id == search_id,
                SearchResult.viewed == False
            )
        ).all()

        print(f"✅ Найдено {len(unviewed)} непросмотренных профилей для поиска {search_id}")
        return unviewed

    except SQLAlchemyError as e:
        print(f"❌ Ошибка при получении непросмотренных профилей: {e}")
        return []
    finally:
        session.close()


def get_one_unviewed_profile(user_id, search_id):
    """Получает ОДИН случайный непросмотренный профиль для данного поиска"""
    session = Session()
    try:
        from sqlalchemy import func

        unviewed_profile = session.query(Profile).join(SearchResult).filter(
            and_(
                SearchResult.user_id == user_id,
                SearchResult.search_id == search_id,
                SearchResult.viewed == False
            )
        ).order_by(func.random()).first()

        return unviewed_profile

    except SQLAlchemyError as e:
        print(f"❌ Ошибка при получении непросмотренного профиля: {e}")
        return None
    finally:
        session.close()