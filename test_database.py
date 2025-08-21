# test_database.py
from database.db_func import (
    get_or_create_user,
    add_searched_profile,
    mark_profile_as_shown,
    add_to_favorites,
    get_favorites,
    close_session
)
from vk_tools.vk_api_func import search_profiles, get_top_photos  # Было from vk_api.vk_api_func

# Тестовые данные
test_user_id = 710245005
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

print("=== ТЕСТ РАБОТЫ С БАЗОЙ ДАННЫХ ===\n")

# 1. Создаем/получаем пользователя
print("1. Работа с пользователем:")
user = get_or_create_user(**test_user_info)
print(f"   User ID: {user.vk_id}")
print(f"   Имя: {user.first_name} {user.last_name}")
print(f"   Город: {user.city}\n")

# 2. Добавляем тестовый профиль
print("2. Добавление тестового профиля:")
test_photos = ['photo123_456', 'photo123_457', 'photo123_458']  # Тестовые фото
profile = add_searched_profile(test_profile, test_photos)
print(f"   Profile ID: {profile.vk_id}\n")

# 3. Помечаем профиль как показанный
print("3. Отметка показанного профиля:")
mark_profile_as_shown(test_user_id, test_profile['vk_id'])
print("   Профиль отмечен как показанный\n")

# 4. Добавляем в избранное
print("4. Добавление в избранное:")
add_to_favorites(test_user_id, test_profile['vk_id'])
print("   Профиль добавлен в избранное\n")

# 5. Получаем избранное
print("5. Получение списка избранного:")
favorites = get_favorites(test_user_id)
print(f"   Найдено в избранном: {len(favorites)} профилей")
for fav in favorites:
    print(f"   - {fav.first_name} {fav.last_name}")

# 6. Закрываем сессию
close_session()
print("\n=== ТЕСТ ЗАВЕРШЕН ===")