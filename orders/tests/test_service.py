from django.test import TestCase
from django.core import mail

from orders.tasks import (send_mail_after_create_order,
                          send_mail_after_change_order,
                          )
from config.celery import app
from orders.models import Order


class TestSentEmailAfterSuccessCreatedOrder(TestCase):
    """Тестирование сервиса по отправке почты в случаи успешного оформления заказа"""

    def setUp(self):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.order = Order.objects.create(first_name='goga', last_name='vova',
                                          email='test@test.com', phone='123213',
                                          address='street', postal_code='232323',
                                          city='Moscow', transport='pickup',
                                          transport_cost=400)

    def test_sent_email_success(self):
        self.assertEqual(send_mail_after_create_order(self.order.id), 1)
        self.assertEqual(mail.outbox[0].subject, f'Заказ № {self.order.id}')
        self.assertEqual(mail.outbox[0].to, ['test@test.com'])


class TestSentEmailAfterChangedOrderStatus(TestCase):
    """Тестирование сервиса по отправке почты после изменения статуса заказа"""

    def setUp(self):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.order = Order.objects.create(first_name='goga', last_name='vova',
                                          email='test1@test.com', phone='123213',
                                          address='street', postal_code='232323',
                                          city='Moscow', transport='pickup',
                                          transport_cost=400)

    def test_sent_email_correctly(self):
        self.assertEqual(send_mail_after_change_order(self.order.id), 1)
        self.assertEqual(mail.outbox[0].subject, f'Заказ № {self.order.id}')
        self.assertIn(
            f'У вашего заказа № {self.order.id} был изменен статус на "Создан"',
            str(mail.outbox[0].message())
        )
        self.assertEqual(mail.outbox[0].to, ['test1@test.com'])
