import tempfile

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from smokeshop.models import Category, Product, Feedback


file_mock = tempfile.NamedTemporaryFile(suffix=".jpg").name


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

    def test_return_str_name_instance_category(self):
        """Проверка правильной вывода инстанса модели в виде строки"""
        self.assertEqual(str(self.category1), 'CategoryTest1')


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
        self.product2 = Product.objects.create(category=self.category1,
                                               name='Product2', slug='product_slug_2',
                                               is_nicotine=False, brand='Brand2',
                                               maker_country='NeBanana', description='text',
                                               weight=50, strength='2', smoking='4',
                                               taste='orange', price=200, image=file_mock)
        self.feedback1 = Feedback.objects.create(product=self.product1,
                                                 author='Goga',
                                                 rating='5')
        self.feedback2 = Feedback.objects.create(product=self.product1,
                                                 author='Vova',
                                                 rating='4')

    def test_urls_from_get_absolute_url(self):
        """Проверка правильной генерации url'a через метод get_absolute_url"""
        calculate_url = self.product1.get_absolute_url()
        self.assertEqual(calculate_url, '/category_slug_1/product_slug_1/')

    def test_return_str_name_instance_product(self):
        """Проверка правильной вывода инстанса модели в виде строки"""
        self.assertEqual(str(self.product1), 'Product1')

    def test_true_calculate_average_rating(self):
        """Проверка метода get_average_rating_to_feedback модели Product 
        на корректный подсчет средней оценки из комментариев"""
        average_value_to_product2 = self.product2.get_average_rating_to_feedback()
        self.assertEqual(average_value_to_product2, 5.0)
        average_value_to_product1 = self.product1.get_average_rating_to_feedback()
        self.assertEqual(average_value_to_product1, 4.5)

    def test_true_calculate_average_rating_after_add_and_delete(self):
        """Проверка метода get_average_rating_to_feedback модели Product
        при добавлении и удалении комментария к товару"""
        self.feedback3 = Feedback.objects.create(product=self.product1,
                                                 author='Dasha',
                                                 rating='5')
        average_value_to_product1 = self.product1.get_average_rating_to_feedback()
        self.assertEqual(average_value_to_product1, 4.7)
        self.feedback3.delete()
        average_value_to_product1 = self.product1.get_average_rating_to_feedback()
        self.assertEqual(average_value_to_product1, 4.5)


class FeedbackTestCase(TestCase):
    """Тестирование добавленой логики в модель Feedback"""

    def test_return_str_name_instance_feedback(self):
        """Проверка правильной вывода инстанса модели в виде строки"""
        self.category = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.product = Product.objects.create(category=self.category,
                                              name='Product1', slug='product_slug_1',
                                              is_nicotine=True, brand='Brand1',
                                              maker_country='Banana', description='text',
                                              weight=100, strength='1', smoking='2',
                                              taste='apple', price=100, image=file_mock)
        self.feedback = Feedback.objects.create(product=self.product,
                                                author='Dasha',
                                                rating='5')
        self.assertEqual(str(self.feedback),
                         f'Dasha, rating - 5 | {timezone.now().strftime("%m-%d-%Y")}')
