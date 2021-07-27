from django.test import TestCase
from django.urls import reverse

from smokeshop.models import Category


class CategoryTest(TestCase):
    """Тестирование добавленой логики в модель Категорий"""

    def setUp(self):
        """Инициализация тестовых данных"""
        self.category1 = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.category2 = Category.objects.create(
            name='CategoryTest2', slug='category_slug_2')

    def test_urls_from_get_absolute_url(self):
        """Проверка правильной генерации url'a через метод get_absolute_url"""
        calculate_url_1 = self.category1.get_absolute_url()
        calculate_url_2 = self.category2.get_absolute_url()
        self.assertEqual(calculate_url_1, '/category_slug_1/')
        self.assertEqual(calculate_url_2, '/category_slug_2/')
