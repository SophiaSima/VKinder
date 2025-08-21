# vk_tools/vk_tools.py
def parse_user_input(text):
    """
    Парсит текстовый ввод пользователя для обработки команд.
    Теперь распознает как текстовые команды, так и команды из кнопок.
    """
    text = text.lower().strip()

    # Текстовые команды
    if text in ['привет', 'начать', 'start', 'hello', 'hi']:
        return 'start'
    elif text in ['дальше', 'следующий', 'next']:
        return 'next'
    elif text in ['избранное', 'favorites', 'моё избранное', 'мое избранное']:
        return 'favorites'
    elif text in ['добавить', 'добавить в избранное', 'в избранное']:
        return 'add_to_favorites'
    elif text in ['главное меню', 'меню', 'начать заново']:
        return 'start'

    # Команды из кнопок (с эмодзи)
    elif 'дальше' in text or '➡️' in text:
        return 'next'
    elif 'избранное' in text or '❤️' in text or '⭐' in text:
        return 'add_to_favorites' if 'в избранное' in text else 'favorites'
    elif 'начать заново' in text or '🔄' in text:
        return 'start'
    elif 'главное меню' in text or '📋' in text:
        return 'start'

    return 'unknown'