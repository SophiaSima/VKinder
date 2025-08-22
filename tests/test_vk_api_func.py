# tests/test_vk_api_func.py
# python3 -m  pytest tests/test_vk_api_func.py
import sys
sys.path.append('../VKinder/vk_tools')
from vk_api_func import search_profiles, get_user_info, get_top_photos

# Тестируем поиск с разными параметрами
test_cases = [
    {"age": 25, "gender": 1, "city": "Москва", "desc": "Девушки 25 лет в Москве"},
    {"age": 30, "gender": 2, "city": "Санкт-Петербург", "desc": "Парни 30 лет в СПб"},
    {"age": 35, "gender": 1, "city": "Новосибирск", "desc": "Девушки 35 лет в Новосибирске"},
    {"age": 40, "gender": 2, "city": "Иркутск", "desc": "Парни 40 лет в Иркутске"}  
]

def test_search_profiles():
    result = []
    for test_case in test_cases:
        profiles = search_profiles(test_case['age'], test_case['gender'], test_case['city'])

        for _, profile in enumerate(profiles[:3]):
            result.append(profile)
    
    assert len(result) == 12

# Тестируем получение информации о пользователе
def test_get_user_info():
    user_info = get_user_info(710245005)
    assert user_info == {'vk_id': 710245005, 'first_name': 'Сергей', 'last_name': 'Петрусенко', 'age': 37, 'gender': 2, 'city': 'Иркутск'}

# Тестируем получение фотографий
def test_top_photos():
    user_info = get_user_info(710245005)
    profiles = search_profiles(user_info['age'], user_info['gender'], user_info['city'])
    photos = get_top_photos(profiles[0]['vk_id'])
    assert len(photos) == 3