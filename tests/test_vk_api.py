# tests/test_vk_api.py
import unittest
from unittest.mock import patch, MagicMock
from vk_tools.vk_api_func import get_user_info, search_profiles, get_top_photos


class TestVKAPI(unittest.TestCase):
    """Тесты для VK API функций"""

    @patch('vk_tools.vk_api_func.make_vk_request')
    def test_get_user_info_success(self, mock_make_request):
        """Тест успешного получения информации о пользователе"""
        # Мокируем ответ VK API
        mock_response = [{
            'id': 12345,
            'first_name': 'Test',
            'last_name': 'User',
            'bdate': '01.01.1990',
            'sex': 2,
            'city': {'title': 'Moscow'}
        }]
        mock_make_request.return_value = mock_response

        user_info = get_user_info(12345)

        self.assertIsNotNone(user_info)
        self.assertEqual(user_info['first_name'], 'Test')
        self.assertEqual(user_info['city'], 'Moscow')
        self.assertEqual(user_info['gender'], 2)

    @patch('vk_tools.vk_api_func.make_vk_request')
    def test_get_user_info_failure(self, mock_make_request):
        """Тест неудачного получения информации о пользователе"""
        mock_make_request.return_value = None

        user_info = get_user_info(12345)

        self.assertIsNone(user_info)

    @patch('vk_tools.vk_api_func.make_vk_request')
    def test_search_profiles(self, mock_make_request):
        """Тест поиска профилей"""
        mock_response = {
            'items': [
                {
                    'id': 67890,
                    'first_name': 'Anna',
                    'last_name': 'Ivanova',
                    'city': {'title': 'Moscow'},
                    'is_closed': False,
                    'photo_max_orig': 'photo_url'
                }
            ]
        }
        mock_make_request.return_value = mock_response

        profiles = search_profiles(25, 2, 'Moscow')

        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0]['first_name'], 'Anna')


if __name__ == '__main__':
    unittest.main()