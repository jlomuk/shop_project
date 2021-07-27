from django.test import TestCase
from django.urls import reverse
from unittest import mock
from django.core.files import File

from smokeshop.models import Category, Product


file_mock = mock.MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'
file_mock.url = '/media/'


class CategoryTest(TestCase):
    """Тестирование добавленой логики в модель Category"""

    def setUp(self):
        """Инициализация тестовых данных (создание категории)"""
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


class ProductTest(TestCase):
    """Тестирование добавленой логики в модель Products"""

    def setUp(self):
        """Инициализация тестовых данных (создание категории и товара)"""
        self.category1 = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.product1 = Product.objects.create(category=self.category1,
                                               name='Product1', slug='product_slug_1',
                                               is_nicotine=True, brand='Brand1',
                                               maker_country='Banana', description='text',
                                               weight=100, strength='1', smoking='2',
                                               taste='apple', price=100, image=file_mock)

    def test_urls_from_get_absolute_url(self):
        """Проверка правильной генерации url'a через метод get_absolute_url"""
        calculate_url = self.product1.get_absolute_url()
        self.assertEqual(calculate_url, '/category_slug_1/product_slug_1/')
