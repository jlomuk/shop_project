from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import tempfile

from smokeshop.models import Category, Product
from cart.services.cart import Cart


file_mock = tempfile.NamedTemporaryFile(suffix=".jpg").name


class CartViewsTests(TestCase):
    """Набор тестов для проверки корректной работы обработчиков, 
    отвечающего за отображение продуктовой корзины, добавления товаров к корзину,
    изменения количества, a также удаления товара из корзины"""

    def setUp(self):
        """Инициализация тестовых данных"""
        self.client1 = Client()
        self.client2 = Client()
        self.get_data_cart_from_session = lambda client: client.session.get(
            settings.CART_ID)
        self.category1 = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.category2 = Category.objects.create(
            name='CategoryTest2', slug='category_slug_2')
        self.product1 = Product.objects.create(category=self.category1,
                                               name='Product1', slug='product_slug_1',
                                               is_nicotine=True, brand='Brand1',
                                               maker_country='Banana', description='text',
                                               weight=100, strength='1', smoking='2',
                                               taste='apple', price=100, image=file_mock)
        self.product2 = Product.objects.create(category=self.category2,
                                               name='Product2', slug='product_slug_2',
                                               is_nicotine=False, brand='Brand2',
                                               maker_country='NeBanana', description='text',
                                               weight=50, strength='2', smoking='4',
                                               taste='orange', price=200, image=file_mock)

    def test_success_init_cart_in_session_users(self):
        """Тест проверяет отсутствие dict корзины до запроса 
        и получение корзины после первого запроса на страницу сайта"""
        self.assertEqual(self.get_data_cart_from_session(self.client1), None)
        response1 = self.client1.get(reverse('cart:cart_detail'))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(self.get_data_cart_from_session(self.client1), {})
        self.assertEqual(self.get_data_cart_from_session(self.client2), None)
        response2 = self.client2.get(reverse('smokeshop:product_list'))
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(self.get_data_cart_from_session(self.client1), {})
        self.assertEqual(self.get_data_cart_from_session(self.client2), {})

    def test_add_product_to_cart(self):
        """Тест проверяет корректное добавления товара в корзину и 
        независимость корзин разных клиентов"""
        url_path = reverse('cart:cart_add', args=[self.product1.id])
        self.assertEqual(self.get_data_cart_from_session(self.client1), None)
        self.assertEqual(self.get_data_cart_from_session(self.client2), None)
        self.client1.get(reverse('smokeshop:product_list'))
        self.client2.get(reverse('smokeshop:product_list'))
        response = self.client1.post(url_path, data={
                                     'quantity': 2, })
        self.assertRedirects(response, reverse(
            'cart:cart_detail'), status_code=302)
        self.assertEqual(self.get_data_cart_from_session(self.client1)[str(self.product1.id)],
                         {'quantity': 2, 'price': '100.00'})
        self.assertEqual(self.get_data_cart_from_session(self.client2), {})

    def test_update_product_to_cart(self):
        """Тест проверяет корректное обновление количества единиц товара в корзине"""
        url_path = reverse('cart:cart_add', args=[self.product1.id])
        self.assertEqual(self.get_data_cart_from_session(self.client1), None)
        self.client1.get(reverse('smokeshop:product_list'))
        response = self.client1.post(url_path, data={
                                     'quantity': 5, 'update': True})
        self.assertRedirects(response, reverse(
            'cart:cart_detail'), status_code=302)
        self.assertEqual(self.get_data_cart_from_session(self.client1)[str(self.product1.id)],
                         {'quantity': 5, 'price': '100.00'})

    def test_delete_product_from_cart(self):
        """Тест проверяет удаление товара из корзины"""
        url_path_add = reverse('cart:cart_add', args=[self.product1.id])
        url_path_delete = reverse(
            'cart:cart_delete_product', args=[self.product1.id])
        self.client1.get(reverse('smokeshop:product_list'))
        self.client1.post(url_path_add, data={'quantity': 5})
        self.assertEqual(self.get_data_cart_from_session(self.client1)[str(self.product1.id)],
                         {'quantity': 5, 'price': '100.00'})
        response = self.client1.post(url_path_delete)
        self.assertRedirects(response, reverse(
            'cart:cart_detail'), status_code=302)
        self.assertEqual(self.get_data_cart_from_session(self.client1), {})

    def test_full_clear_cart(self):
        """Тест полной очистки корзины"""
        url_path_add_product1 = reverse(
            'cart:cart_add', args=[self.product1.id])
        url_path_add_product2 = reverse(
            'cart:cart_add', args=[self.product2.id])
        url_path_cart_clear = reverse('cart:cart_clear')
        self.client1.get(reverse('smokeshop:product_list'))
        self.client1.post(url_path_add_product1, data={'quantity': 5})
        self.client1.post(url_path_add_product2, data={'quantity': 2})
        self.assertEqual(len(self.get_data_cart_from_session(self.client1)), 2)
        response = self.client1.post(url_path_cart_clear)
        self.assertRedirects(response, reverse(
            'smokeshop:product_list'), status_code=302)
        self.assertEqual(self.get_data_cart_from_session(self.client1), {})
