# tests/test_vk_api.py
# python3 -m  pytest tests/test_vk_api.py
import sys
sys.path.append('../VKinder/vk_tools')
from vk_api_func import get_user_info   #, search_profiles, get_top_photos

# Тестируем получение информации о пользователе
def test_get_user_info():
    user_info = get_user_info(710245005)
    assert user_info == {'vk_id': 710245005, 'first_name': 'Сергей', 'last_name': 'Петрусенко', 'age': 37, 'gender': 2, 'city': 'Иркутск'}

# Если город не определился, задаем его вручную
# if user_info and user_info['age']:
#     if not user_info['city']:
#         user_info['city'] = 'Иркутск'
#         print(f"\nГород установлен вручную: {user_info['city']}")

#     # Тестируем поиск профилей
#     print("\nРезультаты поиска:")
#     profiles = search_profiles(user_info['age'], user_info['gender'], user_info['city'])

#     print(f"Найдено профилей: {len(profiles)}")

#     for i, profile in enumerate(profiles[:3]):  # Покажем первые 3 результата
#         print(f"\n{i + 1}. {profile['first_name']} {profile['last_name']}")
#         print(f"   Ссылка: {profile['profile_link']}")

#         # Тестируем получение фотографий
#         photos = get_top_photos(profile['vk_id'])
#         print(f"   Топ-3 фото: {photos}")
# else:
#     print("Не удалось получить информацию для поиска (возраст)")