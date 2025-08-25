# services/search_service.py
"""
Сервис для поиска и работы с избранным.
Содержит основную бизнес-логику приложения.
"""
from vk_tools.vk_api_func import search_profiles, get_top_photos
from database.db_func import (
    get_or_create_profile,
    create_search,
    add_search_result,
    get_unviewed_profiles,
    mark_profile_as_viewed,
    add_to_favorites,
    get_favorites,
    get_one_unviewed_profile
)
from vk_tools.vk_tools import extract_photos_from_json


class SearchService:
    """Сервис для поиска и работы с избранным"""

    @staticmethod
    def initialize_search(user):
        """
        Инициализирует поиск для пользователя
        Возвращает (search, error_message)
        """
        try:
            # Создаем запись о поиске
            search = create_search(
                user_id=user.id,
                city=user.city,
                age_from=max(18, user.age - 5),
                age_to=min(100, user.age + 5),
                gender=1 if user.gender == 2 else 2  # Противоположный пол
            )

            if not search:
                return None, "Ошибка при создании поиска"

            # Ищем профили
            profiles = search_profiles(user.age, user.gender, user.city)

            if not profiles:
                return search, "Не найдено подходящих профилей"

            # Сохраняем найденные профили
            for profile_data in profiles:
                # Получаем топ фото
                photos = get_top_photos(profile_data['vk_id'])

                # Сохраняем профиль в БД
                profile = get_or_create_profile(profile_data, photos)

                if profile:
                    # Добавляем в результаты поиска
                    add_search_result(search.id, profile.id, user.id)

            return search, None

        except Exception as e:
            print(f"❌ Ошибка в SearchService.initialize_search: {e}")
            return None, "Ошибка при инициализации поиска"

    @staticmethod
    def get_next_profile(user_id, search_id):
        """
        Получает следующий непросмотренный профиль
        Возвращает (profile, photos, error_message)
        """
        try:
            # Получаем один непросмотренный профиль
            profile = get_one_unviewed_profile(user_id, search_id)

            if not profile:
                # Если не нашли через новую функцию, пробуем старую для отладки
                unviewed_profiles = get_unviewed_profiles(user_id, search_id)
                print(f"🔍 Найдено непросмотренных профилей: {len(unviewed_profiles)}")
                for i, prof in enumerate(unviewed_profiles, 1):
                    print(f"   {i + 1}. {prof.first_name} {prof.last_name} (ID: {prof.id})")

                if not unviewed_profiles:
                    return None, None, "Нет непросмотренных профилей"

                profile = unviewed_profiles[0]

            print(f"✅ Выбран профиль: {profile.first_name} {profile.last_name}")

            # Помечаем как просмотренный
            success = mark_profile_as_viewed(user_id, profile.id)
            print(f"✅ Профиль отмечен как просмотренный: {success}")

            # Извлекаем фото
            photos = extract_photos_from_json(profile.photos)

            return profile, photos, None

        except Exception as e:
            print(f"❌ Ошибка в SearchService.get_next_profile: {e}")
            return None, None, "Ошибка при получении профиля"

    @staticmethod
    def add_to_favorites(user_id, profile_id):
        """
        Добавляет профиль в избранное
        Возвращает (success, error_message)
        """
        try:
            success = add_to_favorites(user_id, profile_id)
            return success, None if success else "Не удалось добавить в избранное"
        except Exception as e:
            print(f"❌ Ошибка в SearchService.add_to_favorites: {e}")
            return False, "Ошибка при добавлении в избранное"

    @staticmethod
    def get_user_favorites(user_id):
        """
        Получает избранные профили пользователя
        Возвращает (profiles, error_message)
        """
        try:
            favorites = get_favorites(user_id)
            return favorites, None
        except Exception as e:
            print(f"❌ Ошибка в SearchService.get_user_favorites: {e}")
            return [], "Ошибка при получении избранного"