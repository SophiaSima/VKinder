# services/user_service.py
"""
Сервис для работы с пользователями.
Отвечает за получение и обработку данных пользователя.
"""
from vk_tools.vk_api_func import get_user_info
from database.db_func import get_or_create_user
from vk_tools.vk_tools import validate_search_params


class UserService:
    """Сервис для работы с пользователями"""

    @staticmethod
    def get_or_create_user(vk_id):
        """
        Получает или создает пользователя в системе
        Возвращает (user, error_message)
        """
        try:
            # Получаем информацию о пользователе из VK
            user_info = get_user_info(vk_id)
            if not user_info:
                return None, "Не удалось получить информацию о пользователе"

            # Проверяем параметры для поиска
            is_valid, error_msg = validate_search_params(
                user_info['age'],
                user_info['gender'],
                user_info['city']
            )

            if not is_valid:
                return None, error_msg

            # Создаем или получаем пользователя из БД
            user = get_or_create_user(
                vk_id=user_info['vk_id'],
                first_name=user_info['first_name'],
                last_name=user_info['last_name'],
                age=user_info['age'],
                gender=user_info['gender'],
                city=user_info['city']
            )

            return user, None

        except Exception as e:
            print(f"❌ Ошибка в UserService: {e}")
            return None, "Ошибка при обработке данных пользователя"