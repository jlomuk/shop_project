from decimal import Decimal
from django.conf import settings

from smokeshop.models import Product


class Cart:
    """
    Класс реализующий стандартный функционал продуктовой корзины. 
    Данные хранятся в сессии пользователя.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление нового товара в корзину или обновления количества товара 
        в зависимости от значения update_quantity"""
        product_id = str(product.id)
        if product.available:
            if product_id not in self.cart:
                self.cart[product_id] = {
                    'quantity': 0, 'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Помечает сессию как измененную"""
        self.session.modified = True

    def remove(self, product):
        """Удаляет товар по id из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Очищает корзину полностью, удаляя из сессии пользователя Dict корзины """
        del self.session[settings.CART_ID]
        self.save()

    def get_total_price(self):
        """Метод возвращает стоимость всех товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """Итератор возвращает генератор для последовательного перебора 
        всех товаров в корзине"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity'] 
            yield item

    def __len__(self):
        """Возвращает общее количетсва единиц товара в корзине"""
        return sum(item['quantity'] for item in self.cart.values())
