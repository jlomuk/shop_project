from django.test import TestCase
from django.urls import reverse
from unittest import mock
from django.core.files import File

from smokeshop.models import Category, Product


file_mock = mock.MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'
file_mock.url = '/media/'


class ProductListViewTest(TestCase):
    """Набор тестов для проверки корректной работы обработчика, 
    отвечающего за вывод  всего списка товаров, а также по категориям товара"""

    def setUp(self):
        """Инициализация тестовых данных"""
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

    def test_correct_use_template(self):
        """Проверка вьюшки на использование правильного шаблона"""
        response = self.client.get(reverse('smokeshop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'smokeshop/product/product_list.html')

    def test_response_with_all_products(self):
        """Сравнение переданого в контекст шаблона списка всех товаров и 
        Queryset'a из БД"""
        response = self.client.get(reverse('smokeshop:product_list'))
        all_products = Product.objects.all()
        self.assertQuerysetEqual(
            response.context['product_list'], map(repr, all_products))

    def test_response_with_filter_product_by_category(self):
        """Сравнение переданого в контекст шаблона списка отфильтроных 
        товаров по категориям c результатами из БД"""
        response_1 = self.client.get(reverse('smokeshop:product_list_by_category',
                                             args=[self.category1.slug]))
        response_2 = self.client.get(reverse('smokeshop:product_list_by_category',
                                             args=[self.category2.slug]))
        products_by_category_1 = Product.objects.filter(
            category__slug=self.category1.slug)
        products_by_category_2 = Product.objects.filter(
            category__slug=self.category2.slug)
        self.assertQuerysetEqual(response_1.context_data['product_list'],
                                 map(repr, products_by_category_1))
        self.assertQuerysetEqual(response_2.context_data['product_list'],
                                 map(repr, products_by_category_2))

    def test_response_with_products_by_nonexistent_slug(self):
        """Тест на использовании несуществующего слага категории в качестве 
        параметра фильтрации товаров"""
        response = self.client.get(reverse('smokeshop:product_list_by_category',
                                           args=['nonexistent_slug']))
        products_by_nonexistent_slug = Product.objects.filter(
            category__slug='nonexistent_slug')
        self.assertQuerysetEqual(response.context_data['product_list'],
                                 map(repr, products_by_nonexistent_slug))


class ProductDetailViewTest(TestCase):
    """Набор тестов для проверки корректной работы обработчика, 
    отвечающего за вывод детальной информации по товару"""

    def setUp(self):
        """Инициализация тестовых данных"""
        self.category1 = Category.objects.create(
            name='CategoryTest1', slug='category_slug_1')
        self.category2 = Category.objects.create(
            name='CategoryTest2', slug='category_slug_2')
        self.product1 = Product.objects.create(category=self.category1,
                                               name='Product1', slug='product_slug_1',
                                               is_nicotine=True, brand='Brand1',
                                               maker_country='^Banana', description='text',
                                               weight=100, strength='1', smoking='2',
                                               taste='apple', price=100, image=file_mock)
        self.product2 = Product.objects.create(category=self.category2,
                                               name='Product2', slug='product_slug_2',
                                               is_nicotine=False, brand='Brand2',
                                               maker_country='*NeBanana', description='text',
                                               weight=50, strength='2', smoking='4',
                                               taste='orange', price=200, image=file_mock)

    def test_correct_use_template(self):
        """Проверка вьюшки на использование правильного шаблона"""
        response = self.client.get(reverse('smokeshop:product_detail',
                                           args=[self.category2.slug, self.product2.slug]))
        self.assertContains(response, '*NeBanana', status_code=200)
        self.assertTemplateUsed(
            response, 'smokeshop/product/detail.html')

    def test_response_detail_product_success(self):
        """Проверка передачи правильного продукта по слагу в контекст шаблона"""
        response = self.client.get(reverse('smokeshop:product_detail',
                                           args=[self.category1.slug, self.product1.slug]))
        product = Product.objects.get(category__slug=self.category1.slug,
                                      slug=self.product1.slug)
        self.assertContains(response, '^Banana', status_code=200)
        self.assertEqual(response.context_data['product'], product)

    def test_response_detail_product_with_wrong_slug(self):
        """Тест с неправильными слагами категории и продукта"""
        response_1 = self.client.get(reverse('smokeshop:product_detail',
                                             args=[self.category1.slug, 'wrong_slug']))
        response_2 = self.client.get(reverse('smokeshop:product_detail',
                                             args=['wrong_slug', self.product1.slug]))
        self.assertEqual(response_1.status_code, 404)
        self.assertEqual(response_2.status_code, 404)
