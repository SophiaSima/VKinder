# bot/keyboard_utils.py
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_main_keyboard():
    """Создает основную клавиатуру бота"""
    keyboard = VkKeyboard(one_time=False, inline=False)

    keyboard.add_button('❤️ В избранное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('➡️ Дальше', color=VkKeyboardColor.PRIMARY)

    keyboard.add_line()  # Новая строка

    keyboard.add_button('⭐ Мое избранное', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('🔄 Начать заново', color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def get_empty_keyboard():
    """Создает пустую клавиатуру (скрывает предыдущую)"""
    keyboard = VkKeyboard.get_empty_keyboard()
    return keyboard


def get_favorites_keyboard():
    """Создает клавиатуру для работы с избранным"""
    keyboard = VkKeyboard(one_time=False, inline=False)

    keyboard.add_button('❤️ В избранное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('➡️ Дальше', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📋 Главное меню', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()