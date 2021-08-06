import tempfile

from django.test import TestCase, Client
from unittest.mock import patch
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model

from smokeshop.models import Category, Product
from orders.models import Order
from accounts.models import Profile
from orders.service import create_order_pay_action
from cart.services.cart import Cart


file_mock = tempfile.NamedTemporaryFile(suffix=".jpg").name


class InitialDataOrderCreateMixin:
    """Инициализация тестовых данных"""

    def setUp(self):
        # создаем 2-ух юзеров
        user_model = get_user_model()
        self.user = user_model.objects.create_user('user1', 'user1@test.ru', 'password',
                                                   first_name='goga', last_name='gogoff')
        Profile.objects.create(user=self.user, phone=7777777777, city='Moscow')
        self.user2 = user_model.objects.create_user('user2', 'uses2@test.ru', 'password',
                                                    first_name='fofa', last_name='fofoff')
        Profile.objects.create(user=self.user2, phone=12121212, city='Kirov')
        # создаем 4 клиента(2 auth, 2 anon)
        self.client.login(username='user1', password='password')
        self.client_1 = Client()
        self.client_2 = Client()
        self.client_3 = Client()
        self.client_3.login(username='user2', password='password')

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
        self.url_path_product_1 = reverse(
            'cart:cart_add', args=[self.product1.id])
        self.url_path_product_2 = reverse(
            'cart:cart_add', args=[self.product2.id])
        self.client_1.get(reverse('smokeshop:product_list'))
        self.client.get(reverse('smokeshop:product_list'))
        self.client_1.post(self.url_path_product_1, data={'quantity': 2, })
        self.client_1.post(self.url_path_product_2, data={'quantity': 3, })
        self.client.post(self.url_path_product_1, data={'quantity': 2, })

    def _data_for_order_form(self):
        data = {
            'first_name': 'testfirst',
            'last_name': 'testlast',
            'email': 'testemail@goga.ru',
            'phone': '9999999999',
            'address': 'testStreet',
            'postal_code': '112233',
            'city': 'Moscow',
            'transport': 'Courier'
        }
        return data


class OrderTestCase(InitialDataOrderCreateMixin, TestCase):
    """Тесты для проверки корректного создания заказа"""

    def test_get_request_to_create_order_with_products_in_cart(self):
        """запрос на страницу создания заказа с продуктами в корзине"""
        response = self.client_1.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)

    def test_get_request_to_create_order_without_products(self):
        """запрос на страницу создания заказа без продуктов в корзине"""
        response1 = self.client_2.get(reverse('orders:order_create'))
        self.assertEqual(response1.status_code, 404)

    def test_init_profile_informations_auth_user_in_order_create_form(self):
        '''Тест передачи данных из профиля зарегистрирована пользователя,
        в шаблон заказа товара
        '''
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.context_data['form'].initial['first_name'],
                         'goga')
        self.assertEqual(response.context_data['form'].initial['city'],
                         'Moscow')
        self.assertEqual(response.context_data['form'].initial['address'],
                         '')

    @patch('orders.views.create_order_pay_action')
    @patch('orders.views.send_mail_after_create_order')
    def test_create_order_anonimus(self, mock_create_order_pay_action,
                                   mock_send_mail_after_create_order):
        """Проверка корректного создание заказа для анонимного пользователя"""
        url_create_order = reverse('orders:order_create')
        self.assertEqual(Order.objects.count(), 0)
        response = self.client_1.post(url_create_order,
                                      data=self._data_for_order_form())
        self.assertTrue('order_id' in self.client_1.session)
        self.assertRedirects(response, reverse('orders:order_created'))
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().user, None)
        self.assertFalse('order_id' in self.client_1.session)

    @patch('orders.views.create_order_pay_action')
    @patch('orders.views.send_mail_after_create_order')
    def test_create_order_auth_user(self, mock_create_order_pay_action,
                                    mock_send_mail_after_create_order):
        """Проверка корректного создание заказа для авторизированого пользователя"""
        url_create_order = reverse('orders:order_create')
        self.assertEqual(Order.objects.count(), 0)
        response = self.client.post(url_create_order,
                                    data=self._data_for_order_form())
        self.assertTrue('order_id' in self.client.session)
        self.assertRedirects(response, reverse('orders:order_created'))
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().user, self.user)
        self.assertFalse('order_id' in self.client.session)

class TestOrderDetailViewOnHtmlAndPdf(InitialDataOrderCreateMixin, TestCase):

    @patch('orders.views.create_order_pay_action')
    @patch('orders.views.send_mail_after_create_order')
    def _create_new_order_owner_user(self, mock_create_order_pay_action,
                          mock_send_mail_after_create_order):
        url_create_order = reverse('orders:order_create')
        response = self.client.post(url_create_order,
                           data=self._data_for_order_form())

    def test_get_order_detail_for_anonim_user(self):
        self._create_new_order_owner_user()
        url_path = reverse('orders:get_order_detail',
                           args=[self.user.orders.first().id])
        response = self.client_1.get(url_path)
        self.assertEqual(response.status_code, 404)

    def test_get_order_detail_for_owner_user(self):   
        self._create_new_order_owner_user()
        url_path = reverse('orders:get_order_detail',
                           args=[self.user.orders.first().id])
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')

    def test_get_order_detail_for_not_owner_user(self):
        self._create_new_order_owner_user()
        url_path = reverse('orders:get_order_detail',
                           args=[self.user.orders.first().id])
        response = self.client_3.get(url_path)
        self.assertEqual(response.status_code, 404)
