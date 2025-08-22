# tests/test_db_func.py
# python3 -m  pytest tests/test_db_func.py
import sys
sys.path.append('../VKinder/database')
import pytest
from db_func import (
    get_or_create_user,
    add_searched_profile,
    mark_profile_as_shown,
    add_to_favorites,
    get_favorites
)

# Тестовые данные
test_user_id = 710245005
test_photos = ['photo123_456', 'photo123_457', 'photo123_458']
test_user_info = {
    'vk_id': test_user_id,
    'first_name': 'Сергей',
    'last_name': 'Петрусенко',
    'age': 37,
    'gender': 2,
    'city': 'Иркутск'
}

# Тестовый профиль для добавления
test_profile = {
    'vk_id': 123456789,
    'first_name': 'Тест',
    'last_name': 'Профиль',
    'profile_link': 'https://vk.com/id123456789'
}

# Создаем/получаем пользователя
def test_get_or_create_user():
    user = get_or_create_user(**test_user_info)
    assert f'Найден существующий пользователь: {user.first_name} {user.last_name}' or f'Создан новый пользователь: {user.first_name} {user.last_name}'

# Добавляем тестовый профиль
def test_add_searched_profile():
    profile = add_searched_profile(test_profile, test_photos)
    assert f'Добавлен новый профиль: {profile.first_name} {profile.last_name}' or f'Профиль уже существует: {profile.first_name} {profile.last_name}'

# Помечаем профиль как показанный
def test_mark_profile_as_shown():
    mark_profile_as_shown(test_user_id, test_profile['vk_id'])
    assert f'Профиль {test_user_id} отмечен как показанный пользователю {test_profile["vk_id"]}'

# Добавляем в избранное
def test_add_to_favorites():
    add_to_favorites(test_user_id, test_profile['vk_id'])
assert f'Профиль {test_user_id} добавлен в избранное пользователю {test_profile["vk_id"]}' or f'Профиль {test_user_id} уже в избранном у пользователя {test_profile["vk_id"]}'

# Получаем избранное
def test_get_favorites():
    favorites = get_favorites(test_user_id)
    result = {}
    for fav in favorites:
        result = f'{fav.first_name} {fav.last_name}'
    assert result == 'Тест Профиль'