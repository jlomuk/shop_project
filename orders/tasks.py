from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def send_mail_after_create_order(order_id):
    """Отправка письма в случаи успешного оформления заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'Дорогой {order.first_name} {order.last_name}, \n\n' \
        f'Ваш заказ был успешно оформлен.\n' \
        f'Ваш заказ № {order_id}.'
    mail_sent = send_mail(
        subject,
        message,
        'admin@smokeshop.com',
        [order.email]
    )
    return mail_sent
