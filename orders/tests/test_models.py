import tempfile
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from smokeshop.models import Category, Product
from orders.models import Order, OrderItem


file_mock = tempfile.NamedTemporaryFile(suffix=".jpg").name


class OrderTest(TestCase):
    """Тестирование добавленой логики в модели Order"""

    def setUp(self):
        """Инициализация тестовых данных (создание категории, товара, заказа)"""
        """Инициализация тестовых данных (создание категории, товара, заказа)"""
        self.category = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.product_1 = Product.objects.create(category=self.category,
                                                name='Product1', slug='product_slug_1',
                                                is_nicotine=True, brand='Brand1',
                                                maker_country='Banana', description='text',
                                                weight=100, strength='1', smoking='2',
                                                taste='apple', price=100, image=file_mock)
        self.product_2 = Product.objects.create(category=self.category,
                                                name='Product2', slug='product_slug_2',
                                                is_nicotine=False, brand='Brand2',
                                                maker_country='NeBanana', description='text',
                                                weight=50, strength='2', smoking='4',
                                                taste='orange', price=200, image=file_mock)
        self.order = Order.objects.create(first_name='goga', last_name='vova',
                                          email='test@test.com', phone='123213',
                                          address='street', postal_code='232323',
                                          city='Moscow', transport='pickup',
                                          transport_cost=400)
        OrderItem.objects.create(order=self.order, product=self.product_1,
                                 price=100, quantity=4)
        OrderItem.objects.create(order=self.order, product=self.product_2,
                                 price=200, quantity=1)

    def test_return_str_name_instance_order(self):
        """Проверка правильной вывода инстанса модели в виде строки"""
        self.assertEqual(str(self.order), f'Заказ № {self.order.id}')

    def test_calculate_total_cost(self):
        """Проверка подсчета суммы"""
        self.assertEquals(self.order.get_total_cost(), Decimal('1000'))


class OrderItemTest(TestCase):
    """Тестирование добавленой логики в модели OrderItem"""

    def setUp(self):
        """Инициализация тестовых данных (создание категории, товара, заказа)"""
        self.category = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.product = Product.objects.create(category=self.category,
                                              name='Product1', slug='product_slug_1',
                                              is_nicotine=True, brand='Brand1',
                                              maker_country='Banana', description='text',
                                              weight=100, strength='1', smoking='2',
                                              taste='apple', price=100, image=file_mock)
        self.order = Order.objects.create(first_name='goga', last_name='vova',
                                          email='test@test.com', phone='123213',
                                          address='street', postal_code='232323',
                                          city='Moscow', transport='pickup',
                                          transport_cost=400)
        self.item = OrderItem.objects.create(order=self.order, product=self.product,
                                             price=100, quantity=4)

    def test_return_str_name_instance_orderitem(self):
        """Проверка правильной вывода инстанса модели в виде строки"""
        self.assertEqual(str(self.item), str(self.item.id))

    def test_calculate_total_cost(self):
        """Проверка подсчета общей суммы товаров"""
        self.assertEquals(self.item.get_cost(), 400)
