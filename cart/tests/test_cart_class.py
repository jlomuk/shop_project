from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
import tempfile

from smokeshop.models import Category, Product
from cart.services.cart import Cart


file_mock = tempfile.NamedTemporaryFile(suffix=".jpg").name


class CartСlassTests(TestCase):
    """Тесты для проверки верной логики класса корзины"""

    def setUp(self):
        """Инициализация тестовых данных"""
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
        self.cart = Cart(self.client)

    def test_method_add_product(self):
        """Проверка инстанса на добавления товара"""
        self.cart.add(product=self.product1, quantity=3)
        self.assertEqual(len(list(iter(self.cart))), 1)
        self.assertEqual(len(self.cart), 3)
        self.cart.add(product=self.product2, quantity=2)
        self.assertEqual(len(list(iter(self.cart))), 2)
        self.assertEqual(len(self.cart), 5)
        self.cart.add(product=self.product1, quantity=1)
        self.assertEqual(len(list(iter(self.cart))), 2)
        self.assertEqual(len(self.cart), 6)

    def test_method_get_total_price(self):
        """Проверка подсчета общей суммы"""
        self.cart.add(product=self.product1, quantity=3)
        self.cart.add(product=self.product2, quantity=2)
        self.assertEqual(self.cart.get_total_price(), Decimal('700'))

    def test_method_iter(self):
        """Тест корректной структуры и данных в возвращаемом генераторе"""
        self.cart.add(product=self.product1, quantity=3)
        returned_product_from_generator = list(self.cart)[0]
        self.assertListEqual(list(returned_product_from_generator.keys()),
                             ['quantity', 'price', 'product', 'total_price'])
        self.assertEqual(returned_product_from_generator['quantity'], 3)
        self.assertEqual(returned_product_from_generator['price'], Decimal('100'))
        self.assertEqual(returned_product_from_generator['total_price'], Decimal('300'))
        self.assertEqual(returned_product_from_generator['product'], self.product1)
