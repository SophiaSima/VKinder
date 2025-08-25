# tests/test_models_only.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_models import Base, User, Profile, Search, SearchResult


class TestModels(unittest.TestCase):
    """Тесты только для моделей базы данных"""

    @classmethod
    def setUpClass(cls):
        """Настройка тестовой базы данных"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_user_model_creation(self):
        """Тест создания модели User"""
        user = User(
            vk_id=1001,
            first_name="John",
            last_name="Doe",
            age=30,
            gender=2,
            city="New York"
        )
        self.session.add(user)
        self.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.vk_id, 1001)

    def test_profile_model_creation(self):
        """Тест создания модели Profile"""
        profile = Profile(
            vk_id=2001,
            first_name="Jane",
            last_name="Smith",
            profile_link="https://vk.com/id2001",
            photos='["photo1", "photo2"]'
        )
        self.session.add(profile)
        self.session.commit()

        self.assertIsNotNone(profile.id)
        self.assertEqual(profile.last_name, "Smith")

    def test_search_model_creation(self):
        """Тест создания модели Search"""
        search = Search(
            user_id=1,
            city="Moscow",
            age_from=20,
            age_to=35,
            gender=1
        )
        self.session.add(search)
        self.session.commit()

        self.assertIsNotNone(search.id)
        self.assertEqual(search.age_from, 20)

    def test_search_result_model_creation(self):
        """Тест создания модели SearchResult"""
        result = SearchResult(
            search_id=1,
            profile_id=1,
            user_id=1,
            viewed=False,
            liked=True
        )
        self.session.add(result)
        self.session.commit()

        self.assertIsNotNone(result.id)
        self.assertTrue(result.liked)
        self.assertFalse(result.viewed)

    def test_user_profile_relationship(self):
        """Тест связи между пользователями и профилями"""
        # Создаем пользователя
        user = User(
            vk_id=3001,
            first_name="Alice",
            last_name="Johnson",
            age=28,
            gender=1,
            city="London"
        )
        self.session.add(user)
        self.session.commit()

        # Создаем профиль
        profile = Profile(
            vk_id=4001,
            first_name="Bob",
            last_name="Brown",
            profile_link="https://vk.com/id4001",
            photos='[]'
        )
        self.session.add(profile)
        self.session.commit()

        # Создаем поиск
        search = Search(
            user_id=user.id,
            city="London",
            age_from=25,
            age_to=35,
            gender=2
        )
        self.session.add(search)
        self.session.commit()

        # Создаем результат поиска
        result = SearchResult(
            search_id=search.id,
            profile_id=profile.id,
            user_id=user.id,
            viewed=True,
            liked=False
        )
        self.session.add(result)
        self.session.commit()

        # Проверяем связи
        self.assertEqual(result.user_id, user.id)
        self.assertEqual(result.profile_id, profile.id)
        self.assertEqual(result.search_id, search.id)


if __name__ == '__main__':
    unittest.main()