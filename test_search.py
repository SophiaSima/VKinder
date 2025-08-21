# test_search.py
from vk_tools.vk_api_func import search_profiles, get_top_photos  # Было from vk_api.vk_api_func

# Тестируем поиск с разными параметрами
test_cases = [
    {"age": 25, "gender": 1, "city": "Москва", "desc": "Девушки 25 лет в Москве"},
    {"age": 30, "gender": 2, "city": "Санкт-Петербург", "desc": "Парни 30 лет в СПб"},
    {"age": 35, "gender": 1, "city": "Новосибирск", "desc": "Девушки 35 лет в Новосибирске"},
    {"age": 40, "gender": 2, "city": "Иркутск", "desc": "Парни 40 лет в Иркутске"}  # Ваш город!
]

for test_case in test_cases:
    print(f"\n{'=' * 50}")
    print(f"Тест: {test_case['desc']}")
    print(f"{'=' * 50}")

    profiles = search_profiles(test_case['age'], test_case['gender'], test_case['city'])
    print(f"Найдено профилей: {len(profiles)}")

    for i, profile in enumerate(profiles[:3]):  # Первые 3 результата
        print(f"\n{i + 1}. {profile['first_name']} {profile['last_name']}")
        print(f"   Ссылка: {profile['profile_link']}")

        # Проверяем фото
        photos = get_top_photos(profile['vk_id'])
        print(f"   Фото: {len(photos)} шт.")
        if photos:
            print(f"   Пример фото: {photos[0]}")