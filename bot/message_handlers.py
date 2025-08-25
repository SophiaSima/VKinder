# bot/message_handlers.py
"""
Обработчики сообщений для бота VKinder.
"""
from bot.keyboard_utils import create_main_keyboard
from bot.texts import *
from services.user_service import UserService
from services.search_service import SearchService
from config import MAX_PHOTOS


class MessageHandlers:
    """Класс для обработки сообщений бота"""

    def __init__(self, vk, session):
        self.vk = vk
        self.session = session
        self.user_states = {}  # Хранение состояний пользователей

    def handle_start(self, user_id):
        """Обработка команды начала работы"""
        try:
            # Отправляем приветственное сообщение
            self.vk.messages.send(
                user_id=user_id,
                message=WELCOME_MESSAGE,
                random_id=0
            )

            # Получаем или создаем пользователя
            user, error = UserService.get_or_create_user(user_id)

            if error:
                self.vk.messages.send(
                    user_id=user_id,
                    message=ERROR_PROFILE_INFO + f"\n\n{error}",
                    random_id=0,
                    keyboard=create_main_keyboard().get_keyboard()
                )
                return None

            # Отправляем информацию о профиле
            gender_text = "женский" if user.gender == 1 else "мужской"
            self.vk.messages.send(
                user_id=user_id,
                message=PROFILE_INFO_RECEIVED.format(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    age=user.age,
                    city=user.city,
                    gender=gender_text
                ),
                random_id=0
            )

            # Инициализируем поиск
            search, search_error = SearchService.initialize_search(user)

            if search_error:
                self.vk.messages.send(
                    user_id=user_id,
                    message=search_error,
                    random_id=0,
                    keyboard=create_main_keyboard().get_keyboard()
                )
                return None

            # Сохраняем состояние пользователя
            self.user_states[user_id] = {
                'user_id': user.id,
                'search_id': search.id,
                'current_profile': None
            }

            # Показываем первый профиль
            self.show_next_profile(user_id)

            return user

        except Exception as e:
            print(f"❌ Ошибка в handle_start: {e}")
            self.vk.messages.send(
                user_id=user_id,
                message=ERROR_GENERIC,
                random_id=0
            )

    def show_next_profile(self, user_id):
        """Показывает следующий профиль"""
        try:
            if user_id not in self.user_states:
                self.handle_start(user_id)
                return

            state = self.user_states[user_id]
            profile, photos, error = SearchService.get_next_profile(
                state['user_id'],
                state['search_id']
            )

            if error:
                self.vk.messages.send(
                    user_id=user_id,
                    message=NO_MORE_PROFILES,
                    random_id=0,
                    keyboard=create_main_keyboard().get_keyboard()
                )
                return

            # Сохраняем текущий профиль
            state['current_profile'] = profile

            # Форматируем сообщение
            message = PROFILE_MESSAGE.format(
                first_name=profile.first_name,
                last_name=profile.last_name,
                profile_link=profile.profile_link,
                photos_count=len(photos) if photos else 0
            )

            # Отправляем сообщение с фото
            attachment = ','.join(photos[:MAX_PHOTOS]) if photos else ''

            self.vk.messages.send(
                user_id=user_id,
                message=message,
                attachment=attachment,
                random_id=0,
                keyboard=create_main_keyboard().get_keyboard()
            )

        except Exception as e:
            print(f"❌ Ошибка в show_next_profile: {e}")
            self.vk.messages.send(
                user_id=user_id,
                message=ERROR_GENERIC,
                random_id=0
            )

    def handle_add_to_favorites(self, user_id):
        """Обработка добавления в избранное"""
        try:
            if (user_id not in self.user_states or
                    not self.user_states[user_id].get('current_profile')):
                self.vk.messages.send(
                    user_id=user_id,
                    message="Сначала начни поиск!",
                    random_id=0,
                    keyboard=create_main_keyboard().get_keyboard()
                )
                return

            state = self.user_states[user_id]
            profile_id = state['current_profile'].id

            success, error = SearchService.add_to_favorites(
                state['user_id'],
                profile_id
            )

            if success:
                self.vk.messages.send(
                    user_id=user_id,
                    message=FAVORITE_ADDED,
                    random_id=0
                )
            else:
                self.vk.messages.send(
                    user_id=user_id,
                    message=FAVORITE_ALREADY_ADDED if "уже" in str(error) else error,
                    random_id=0
                )

        except Exception as e:
            print(f"❌ Ошибка в handle_add_to_favorites: {e}")
            self.vk.messages.send(
                user_id=user_id,
                message=ERROR_GENERIC,
                random_id=0
            )

    def handle_show_favorites(self, user_id):
        """Показывает избранное пользователя"""
        try:
            if user_id not in self.user_states:
                self.vk.messages.send(
                    user_id=user_id,
                    message="Сначала начни поиск!",
                    random_id=0,
                    keyboard=create_main_keyboard().get_keyboard()
                )
                return

            state = self.user_states[user_id]
            favorites, error = SearchService.get_user_favorites(state['user_id'])

            if error:
                self.vk.messages.send(
                    user_id=user_id,
                    message=error,
                    random_id=0
                )
                return

            if not favorites:
                self.vk.messages.send(
                    user_id=user_id,
                    message=FAVORITES_EMPTY,
                    random_id=0
                )
                return

            # Форматируем список избранного
            message = FAVORITES_LIST
            for i, profile in enumerate(favorites, 1):
                message += f"{i}. {profile.first_name} {profile.last_name}\n"
                message += f"   Ссылка: {profile.profile_link}\n\n"

            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=0,
                keyboard=create_main_keyboard().get_keyboard()
            )

        except Exception as e:
            print(f"❌ Ошибка в handle_show_favorites: {e}")
            self.vk.messages.send(
                user_id=user_id,
                message=ERROR_GENERIC,
                random_id=0
            )

    def handle_help(self, user_id):
        """Показывает справку по командам"""
        self.vk.messages.send(
            user_id=user_id,
            message=HELP_MESSAGE,
            random_id=0,
            keyboard=create_main_keyboard().get_keyboard()
        )