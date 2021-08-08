import os
import stripe
import datetime
import xlsxwriter
import weasyprint
from io import BytesIO  
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


from .models import OrderItem
from cart.services.cart import Cart


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def forming_report_order_to_pdf(order, file=False):
    """функция формирует pdf документ из html шаблона"""
    if file: 
        response = BytesIO()
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    html = render_to_string('orders/pdf.html', {'order': order})
    stylesheets = [weasyprint.CSS(os.path.join(
        str(settings.STATIC_ROOT) + '/css/pdf.css'))]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    return response


def initial_response_for_xlsx():
    """Создания ответа для передачи созданого xlsx"""
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y')
    content_disposition = f'attachment; filename=orders_{timestamp}.xlsx'
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = content_disposition
    return response


def create_report_to_xlsx_for_orders(response, opts, products, queryset):
    """формирование xlsx отчета по заказам"""
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    fields = [field for field in opts.get_fields() if not field.one_to_many]
    header_list = [field.name for field in fields]
    for product in products:
        header_list.append(f'{product.name} qty')
        header_list.append(f'{product.name} price')

    header_list.append('order_price_total')
    for column, item in enumerate(header_list):
        worksheet.write(0, column, item)

    for row, obj in enumerate(queryset):
        prod_tracker = {product.name: {'qty': 0, 'price': 0}
                        for product in products}
        order_items = obj.items.all()
        for item in order_items:
            prod_tracker[item.product.name]['qty'] = item.quantity
            prod_tracker[item.product.name]['price'] = item.price
        data_row = []
        order_price_total = 0
        for field in fields:
            value = getattr(obj, field.name)
            if field.name == 'transport_cost':
                order_price_total += value
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            if isinstance(value, get_user_model()):
                value = str(value)
            data_row.append(value)

        for product in prod_tracker:
            for qty_price in prod_tracker[product]:
                data_row.append(prod_tracker[product][qty_price])
            order_price_total += (
                prod_tracker[product]['qty'] * prod_tracker[product]['price']
            )
        data_row.append(order_price_total)
        for column, item in enumerate(data_row):
            worksheet.write(row + 1, column, item)
    workbook.close()
    return response


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


def get_customer_profile(request):
    """Возвращает информацию из профиля покупателя для формы"""
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': request.user.profile.phone,
        'address': request.user.profile.address,
        'postal_code': request.user.profile.postal_code,
        'city': request.user.profile.city,
    }
    return initial_data
