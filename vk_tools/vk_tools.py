def parse_user_input(text):
    """
    Парсит текстовый ввод пользователя для обработки команд.
    Распознает как текстовые команды, так и команды из кнопок.
    """
    if not text:
        return 'unknown'

    text = text.lower().strip()

    # Текстовые команды
    if text in ['привет', 'начать', 'start', 'hello', 'hi', 'бот']:
        return 'start'
    elif text in ['дальше', 'следующий', 'next', 'продолжить']:
        return 'next'
    elif text in ['избранное', 'favorites', 'моё избранное', 'мое избранное', 'список избранного']:
        return 'favorites'
    elif text in ['добавить', 'добавить в избранное', 'в избранное', 'лайк']:
        return 'add_to_favorites'
    elif text in ['главное меню', 'меню', 'начать заново', 'рестарт']:
        return 'start'
    elif text in ['помощь', 'help', 'команды']:
        return 'help'

    # Команды из кнопок (с эмодзи)
    elif 'дальше' in text or '➡️' in text or 'следующий' in text:
        return 'next'
    elif 'избранное' in text or '❤️' in text or '⭐' in text:
        return 'add_to_favorites' if 'в избранное' in text or 'добавить' in text else 'favorites'
    elif 'начать заново' in text or '🔄' in text or 'рестарт' in text:
        return 'start'
    elif 'главное меню' in text or '📋' in text or 'меню' in text:
        return 'start'
    elif 'помощь' in text or '❓' in text:
        return 'help'

    return 'unknown'


def validate_search_params(age, gender, city):
    """
    Проверяет параметры поиска на валидность.
    Возвращает (is_valid, error_message)
    """
    if not age:
        return False, "Возраст не указан. Укажите дату рождения в настройках VK."

    if age < 18:
        return False, "Поиск доступен только для пользователей старше 18 лет."

    if age > 100:
        return False, "Указан некорректный возраст."

    if gender not in [1, 2]:
        return False, "Пол не указан или указан некорректно."

    if not city:
        return False, "Город не указан. Укажите город в настройках VK."

    return True, ""


def format_profile_message(profile, photos_count=0):
    """
    Форматирует сообщение с информацией о профиле.
    """
    message = f"👤 {profile['first_name']} {profile['last_name']}\n"
    message += f"🔗 Ссылка: {profile['profile_link']}\n"

    if photos_count > 0:
        message += f"📸 Фотографий: {photos_count}\n"

    return message


def format_favorites_list(favorites):
    """
    Форматирует список избранных профилей.
    """
    if not favorites:
        return "В избранном пока никого нет 😢"

    message = "⭐ Ваше избранное:\n\n"
    for i, profile in enumerate(favorites, 1):
        message += f"{i}. {profile.first_name} {profile.last_name}\n"
        message += f"   Ссылка: {profile.profile_link}\n\n"

    return message


def extract_photos_from_json(photos_json):
    """
    Извлекает список фото из JSON-строки.
    """
    import json
    try:
        if photos_json:
            return json.loads(photos_json)
        return []
    except (json.JSONDecodeError, TypeError):
        return []