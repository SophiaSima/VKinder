# bot/message_handlers.py
from bot.keyboard_utils import get_main_keyboard, get_empty_keyboard, get_favorites_keyboard
from database.db_func import get_or_create_user, add_to_favorites, get_favorites
# Измените импорты
from vk_tools.vk_api_func import get_user_info, search_profiles, get_top_photos  # Было from vk_api.vk_api_func
from vk_tools.vk_tools import parse_user_input  # Было from vk_api.vk_tools


class BotState:
    """Класс для хранения состояния бота"""

    def __init__(self):
        self.user_states = {}  # user_id -> state_data
        self.search_results = {}  # user_id -> [profiles]
        self.current_index = {}  # user_id -> current_profile_index

    def get_user_state(self, user_id):
        """Получает состояние пользователя"""
        if user_id not in self.user_states:
            self.user_states[user_id] = {'state': 'start', 'data': {}}
        return self.user_states[user_id]

    def set_user_state(self, user_id, state, data=None):
        """Устанавливает состояние пользователя"""
        if data is None:
            data = {}
        self.user_states[user_id] = {'state': state, 'data': data}


# Глобальный объект состояния бота
bot_state = BotState()


def handle_start(user_id, message_text):
    """Обработчик команды начала работы"""
    user_info = get_user_info(user_id)

    if not user_info:
        return "Не могу получить ваши данные из VK. Проверьте настройки приватности.", get_empty_keyboard()

    if not user_info.get('city'):
        return "В вашем профиле не указан город. Укажите город в настройках VK и попробуйте снова.", get_empty_keyboard()

    # Сохраняем пользователя в БД
    user = get_or_create_user(**user_info)

    # Ищем кандидатов
    profiles = search_profiles(user_info['age'], user_info['gender'], user_info['city'])

    if not profiles:
        return "К сожалению, не найдено подходящих анкет. Попробуйте позже.", get_empty_keyboard()

    # Сохраняем результаты поиска
    bot_state.search_results[user_id] = profiles
    bot_state.current_index[user_id] = 0
    bot_state.set_user_state(user_id, 'browsing')

    return show_next_profile(user_id)


def show_next_profile(user_id):
    """Показывает следующего кандидата"""
    if user_id not in bot_state.search_results or user_id not in bot_state.current_index:
        return handle_start(user_id, "")

    profiles = bot_state.search_results[user_id]
    current_index = bot_state.current_index[user_id]

    if current_index >= len(profiles):
        return "Анкеты закончились! 🎉 Нажмите '🔄 Начать заново' для нового поиска.", get_main_keyboard()

    profile = profiles[current_index]

    # Получаем фотографии
    photos = get_top_photos(profile['vk_id'])

    # Формируем сообщение
    message = f"{profile['first_name']} {profile['last_name']}\n"
    message += f"Ссылка: {profile['profile_link']}\n\n"

    # Формируем attachment для фото
    attachment = ','.join(photos) if photos else ""

    return message, get_main_keyboard(), attachment


def handle_add_to_favorites(user_id):
    """Добавление текущего профиля в избранное"""
    if user_id not in bot_state.search_results or user_id not in bot_state.current_index:
        return "Сначала начните поиск!", get_main_keyboard()

    current_index = bot_state.current_index[user_id]
    profile = bot_state.search_results[user_id][current_index]

    success = add_to_favorites(user_id, profile['vk_id'])

    if success:
        return "✅ Добавлено в избранное!", get_main_keyboard()
    else:
        return "❌ Уже в избранном!", get_main_keyboard()


def handle_show_favorites(user_id):
    """Показывает избранное пользователя"""
    favorites = get_favorites(user_id)

    if not favorites:
        return "В избранном пока никого нет 😢", get_main_keyboard()

    message = "⭐ Ваше избранное:\n\n"
    for i, profile in enumerate(favorites, 1):
        message += f"{i}. {profile.first_name} {profile.last_name}\n"
        message += f"   Ссылка: {profile.profile_link}\n\n"

    return message, get_favorites_keyboard()


# bot/message_handlers.py
def handle_message(user_id, message_text):
    """Основной обработчик сообщений"""
    print(f"Обработка сообщения: '{message_text}' от пользователя {user_id}")

    command = parse_user_input(message_text)
    current_state = bot_state.get_user_state(user_id)['state']

    print(f"Распознанная команда: '{command}', текущее состояние: '{current_state}'")

    if command == 'start' or current_state == 'start':
        print("Запуск handle_start...")
        return handle_start(user_id, message_text)

    # ... остальной код без изменений

    elif command == 'add_to_favorites':
        return handle_add_to_favorites(user_id)

    elif command == 'favorites':
        return handle_show_favorites(user_id)

    elif command == 'next':
        # Увеличиваем индекс и показываем следующего
        if user_id in bot_state.current_index:
            bot_state.current_index[user_id] += 1
        return show_next_profile(user_id)

    else:
        return "Не понимаю команду 😢 Используйте кнопки ниже!", get_main_keyboard()