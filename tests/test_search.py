# tests/test_search_service.py
import unittest
from unittest.mock import patch, MagicMock
from services.search_service import SearchService
from database.db_models import User


class TestSearchService(unittest.TestCase):
    """Тесты для сервиса поиска"""

    def setUp(self):
        """Начальные данные для тестов"""
        self.user = User(
            id=1,
            vk_id=12345,
            first_name="Test",
            last_name="User",
            age=25,
            gender=2,
            city="Moscow"
        )

    @patch('services.search_service.search_profiles')
    @patch('services.search_service.get_top_photos')
    @patch('services.search_service.get_or_create_profile')
    @patch('services.search_service.create_search')
    @patch('services.search_service.add_search_result')
    def test_initialize_search_success(self, mock_add_result, mock_create_search,
                                       mock_get_profile, mock_get_photos, mock_search_profiles):
        """Тест успешной инициализации поиска"""
        # Мокируем зависимости
        mock_search_profiles.return_value = [
            {'vk_id': 67890, 'first_name': 'Anna', 'last_name': 'Ivanova', 'profile_link': 'test_link'}
        ]
        mock_get_photos.return_value = ['photo1', 'photo2']

        mock_profile = MagicMock()
        mock_profile.id = 1
        mock_get_profile.return_value = mock_profile

        mock_search = MagicMock()
        mock_search.id = 1
        mock_create_search.return_value = mock_search

        mock_add_result.return_value = True

        search, error = SearchService.initialize_search(self.user)

        self.assertIsNotNone(search)
        self.assertIsNone(error)
        mock_search_profiles.assert_called_once()
        mock_get_photos.assert_called_once()

    @patch('services.search_service.search_profiles')
    @patch('services.search_service.create_search')
    def test_initialize_search_no_profiles(self, mock_create_search, mock_search_profiles):
        """Тест инициализации поиска без найденных профилей"""
        mock_search_profiles.return_value = []

        mock_search = MagicMock()
        mock_search.id = 1
        mock_create_search.return_value = mock_search

        search, error = SearchService.initialize_search(self.user)

        self.assertIsNotNone(search)
        self.assertEqual(error, "Не найдено подходящих профилей")

    @patch('services.search_service.get_unviewed_profiles')
    @patch('services.search_service.mark_profile_as_viewed')
    @patch('services.search_service.extract_photos_from_json')
    def test_get_next_profile(self, mock_extract_photos, mock_mark_viewed, mock_get_unviewed):
        """Тест получения следующего профиля"""
        # Мокируем зависимости
        mock_profile = MagicMock()
        mock_profile.id = 1
        mock_profile.first_name = "Anna"
        mock_profile.last_name = "Ivanova"
        mock_profile.photos = '[]'

        mock_get_unviewed.return_value = [mock_profile]
        mock_mark_viewed.return_value = True
        mock_extract_photos.return_value = ['photo1', 'photo2']

        profile, photos, error = SearchService.get_next_profile(1, 1)

        self.assertIsNotNone(profile)
        self.assertEqual(len(photos), 2)
        self.assertIsNone(error)

    @patch('services.search_service.get_unviewed_profiles')
    def test_get_next_profile_no_profiles(self, mock_get_unviewed):
        """Тест получения профиля когда нет непросмотренных"""
        mock_get_unviewed.return_value = []

        profile, photos, error = SearchService.get_next_profile(1, 1)

        self.assertIsNone(profile)
        self.assertIsNone(photos)
        self.assertEqual(error, "Нет непросмотренных профилей")

    @patch('services.search_service.add_to_favorites')
    def test_add_to_favorites_success(self, mock_add_favorites):
        """Тест добавления в избранное"""
        mock_add_favorites.return_value = True

        success, error = SearchService.add_to_favorites(1, 1)

        self.assertTrue(success)
        self.assertIsNone(error)

    @patch('services.search_service.add_to_favorites')
    def test_add_to_favorites_failure(self, mock_add_favorites):
        """Тест неудачного добавления в избранное"""
        mock_add_favorites.return_value = False

        success, error = SearchService.add_to_favorites(1, 1)

        self.assertFalse(success)
        self.assertEqual(error, "Не удалось добавить в избранное")

    @patch('services.search_service.get_favorites')
    def test_get_user_favorites(self, mock_get_favorites):
        """Тест получения избранного"""
        mock_profile = MagicMock()
        mock_get_favorites.return_value = [mock_profile]

        favorites, error = SearchService.get_user_favorites(1)

        self.assertEqual(len(favorites), 1)
        self.assertIsNone(error)

    @patch('services.search_service.get_favorites')
    def test_get_user_favorites_empty(self, mock_get_favorites):
        """Тест получения пустого избранного"""
        mock_get_favorites.return_value = []

        favorites, error = SearchService.get_user_favorites(1)

        self.assertEqual(len(favorites), 0)
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()