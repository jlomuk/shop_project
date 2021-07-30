from django.test import TestCase, Client
from decimal import Decimal
from django.urls import reverse
import tempfile

from smokeshop.models import Category, Product
from cart.services.cart import Cart


file_mock = tempfile.NamedTemporaryFile(suffix=".jpg").name


class OrderTestCase(TestCase):
    """Тесты для проверки корректного создания заказа"""

    def setUp(self):
        """Инициализация тестовых данных"""
        self.client_1 = Client()
        self.client_2 = Client()
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
        self.url_path_product_1 = reverse('cart:cart_add', args=[self.product1.id])
        self.url_path_product_2 = reverse('cart:cart_add', args=[self.product2.id])
        self.client_1.get(reverse('smokeshop:product_list'))
        self.client_1.post(self.url_path_product_1, data={'quantity': 2, })
        self.client_1.post(self.url_path_product_2, data={'quantity': 3, })


    def test_get_request_order_create_with_products_in_cart(self):
        response = self.client_1.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)

    def test_get_request_order_create_without_products(self):
        response1 = self.client_2.get(reverse('orders:order_create'))
        self.assertEqual(response1.status_code, 404)


