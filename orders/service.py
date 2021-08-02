from decimal import Decimal
import stripe

from django.conf import settings

from .models import OrderItem
from cart.services.cart import Cart


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def _get_customer(request, order):
    """Получение данных покупателя для оплаты"""
    customer = stripe.Customer.create(
        email=order.email,
        source=request.POST['stripeToken']
    )
    return customer


def create_order_pay_action(request, order):
    """Проведение оплаты заказа"""
    charge = stripe.Charge.create(
        customer=_get_customer(request, order),
        amount=int(order.get_total_cost() * 100),
        currency='rub',
        description=order,
    )
    print(charge)
    return charge


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
