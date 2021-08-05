from celery import shared_task
from django.core.mail import send_mail, EmailMessage

from .models import Order
from .service import forming_report_order_to_pdf


@shared_task
def send_mail_after_create_order(order_id):
    """Отправка письма в случаи успешного оформления заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'Дорогой {order.first_name} {order.last_name}, \n\n' \
        f'Ваш заказ был успешно оформлен.\n' \
        f'Ваш заказ № {order_id}.'
    email = EmailMessage(
        subject,
        message,
        'admin@smokeshop.com',
        [order.email]
    )
    file = forming_report_order_to_pdf(order, file=True)
    email.attach(f'Заказ_{order_id}.pdf', file.getvalue(), 'application/pdf')
    return email.send()


@shared_task
def send_mail_after_change_order(order_id):
    """Отправка письма в случаи изменения статуса заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'Дорогой {order.first_name} {order.last_name}, \n\n' \
        f'У вашего заказа № {order_id} был изменен статус на ' \
        f'"{order.get_status_display()}"'
    mail_sent = send_mail(
        subject,
        message,
        'admin@smokeshop.com',
        [order.email]
    )
    return mail_sent
