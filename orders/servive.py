from decimal import Decimal

from django.conf import settings

from .models import OrderItem
from cart.services.cart import Cart


def calculate_transport_cost(order):
    """Возвращает стоимость в зависимости от типа доставки"""
    cost = Decimal('0')
    if order.transport == "Courier":
        cost = Decimal(settings.TRANSPORT_COST)
    return cost


def add_products_to_order_from_cart(obj, order):
    """Добавление к сформированному заказу всех позиций товара из корзины"""
    cart = Cart(obj.request)
    for product in cart:
        OrderItem.objects.create(
            order=order,
            product=product['product'],
            price=product['price'],
            quantity=product['quantity']
        )
    cart.clear()
