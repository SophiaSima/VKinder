import requests
from config import USER_TOKEN, API_VERSION, MAX_PHOTOS
import time

# Базовый URL для всех запросов к API VK
BASE_URL = 'https://api.vk.com/method/'


def make_vk_request(method, params):
    """
    Универсальная функция для выполнения запросов к VK API.
    Обрабатывает ошибки и ограничение по количеству запросов.
    """
    params['access_token'] = USER_TOKEN
    params['v'] = API_VERSION

    try:
        response = requests.get(BASE_URL + method, params=params)
        data = response.json()

        # Проверка на ошибки API VK
        if 'error' in data:
            error_msg = data['error'].get('error_msg', 'Unknown VK API error')
            print(f"❌ Ошибка VK API ({method}): {error_msg}")
            return None

        # Проверка на стандартные HTTP ошибки
        response.raise_for_status()

        return data['response']

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети при запросе к {method}: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка при запросе к {method}: {e}")

    return None


def get_user_info(user_id):
    """
    Получает информацию о пользователе по его ID.
    Возвращает словарь с данными или None в случае ошибки.
    """
    params = {
        'user_ids': user_id,
        'fields': 'city,sex,bdate,home_town'  # Запрашиваем город, пол, дату рождения и родной город
    }

    response = make_vk_request('users.get', params)

    if response and len(response) > 0:
        user_data = response[0]

        # Обрабатываем дату рождения для вычисления возраста
        age = None
        bdate = user_data.get('bdate')
        if bdate and len(bdate.split('.')) == 3:
            birth_year = int(bdate.split('.')[2])
            current_year = time.localtime().tm_year
            age = current_year - birth_year

        # Получаем название города
        city_name = None
        if 'city' in user_data:
            city_name = user_data['city']['title']
        elif 'home_town' in user_data and user_data['home_town']:
            city_name = user_data['home_town']

        # Определяем пол (1 - женский, 2 - мужской, 0 - не указан)
        gender = user_data.get('sex', 0)

        return {
            'vk_id': user_data['id'],
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'age': age,
            'gender': gender,
            'city': city_name
        }

    return None


def search_profiles(age, gender, city, offset=0):
    """
    Ищет пользователей по заданным критериям.
    Ищет противоположный пол.
    """
    # Определяем противоположный пол для поиска
    search_gender = 1 if gender == 2 else 2

    params = {
        'count': 10,  # Количество результатов за один запрос
        'offset': offset,  # Смещение для пагинации
        'fields': 'city,photo_max_orig,is_closed',
        'age_from': max(18, age - 5) if age else 18,  # Разброс возраста ±5 лет
        'age_to': min(100, age + 5) if age else 45,
        'sex': search_gender,
        'hometown': city,  # Родной город
        'has_photo': 1,  # Только с фотографией
        'status': 6,  # В активном поиске
        'sort': 0  # По популярности
    }

    response = make_vk_request('users.search', params)

    if response and 'items' in response:
        # Фильтруем результаты: только с указанным городом и с фото
        filtered_profiles = []
        for profile in response['items']:
            # Проверяем, что город совпадает и профиль не закрыт
            profile_city = None
            if profile.get('city'):
                profile_city = profile['city']['title']

            if (profile_city and profile_city == city and
                    not profile['is_closed'] and
                    profile.get('photo_max_orig')):
                filtered_profiles.append({
                    'vk_id': profile['id'],
                    'first_name': profile.get('first_name', ''),
                    'last_name': profile.get('last_name', ''),
                    'profile_link': f"https://vk.com/id{profile['id']}"
                })

        return filtered_profiles

    return []


def get_top_photos(user_id, count=MAX_PHOTOS):
    """
    Получает топ-N фотографий пользователя по количеству лайков.
    """
    params = {
        'owner_id': user_id,
        'album_id': 'profile',  # Фотографии из профиля
        'extended': 1,  # Получать дополнительную информацию (лайки, комментарии)
        'count': 100  # Достаточно большое количество для выбора
    }

    response = make_vk_request('photos.get', params)

    if response and 'items' in response:
        # Сортируем фотографии по количеству лайков (по убыванию)
        photos = response['items']
        photos.sort(key=lambda x: x['likes']['count'], reverse=True)

        # Берем топ-N фотографий
        top_photos = photos[:count]

        # Формируем список ID фотографий в нужном формате для attachment
        photo_attachments = []
        for photo in top_photos:
            photo_id = f"photo{photo['owner_id']}_{photo['id']}"
            photo_attachments.append(photo_id)

        return photo_attachments

    return []


def get_city_id(city_name):
    """
    Получает ID города по названию.
    """
    params = {
        'q': city_name,
        'count': 1
    }

    response = make_vk_request('database.getCities', params)

    if response and 'items' in response and len(response['items']) > 0:
        return response['items'][0]['id']

    return None