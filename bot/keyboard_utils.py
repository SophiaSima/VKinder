# bot/keyboard_utils.py
"""
Утилиты для создания клавиатур VK бота.
"""
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bot.texts import *


def create_main_keyboard():
    """
    Создает основную клавиатуру для бота.
    """
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button(BUTTON_NEXT, color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(BUTTON_ADD_TO_FAVORITES, color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()
    keyboard.add_button(BUTTON_FAVORITES, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(BUTTON_MENU, color=VkKeyboardColor.SECONDARY)

    keyboard.add_line()
    keyboard.add_button(BUTTON_HELP, color=VkKeyboardColor.NEGATIVE)

    return keyboard


def create_empty_keyboard():
    """
    Создает пустую клавиатуру (скрывает предыдущую).
    """
    keyboard = VkKeyboard.get_empty_keyboard()
    return keyboard