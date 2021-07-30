from django.db import models

from smokeshop.models import Product


class Order(models.Model):
    """Модель для хранения данных клиентского заказа"""

    ORDER_STATUS = [
        ('Created', 'Создан'),
        ('Processing', 'В обработке'),
        ('Shipped', 'Отправлен'),
        ('Ready pickup', 'Готов к выдачи'),
        ('Completed', 'Завершен'),
    ]

    TRANSPORT = [
        ('Courier', 'Курьер'),
        ('pickup', 'Самовывоз'),
    ]

    first_name = models.CharField(
        max_length=100, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=100, verbose_name='Фамилия'
    )
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(
        max_length=20, verbose_name='Телефон'
    )
    address = models.CharField(
        max_length=250, verbose_name='Адрес'
    )
    postal_code = models.CharField(
        max_length=20, verbose_name='Индекс'
    )
    city = models.CharField(
        max_length=100, verbose_name='Город'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан'
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Обновлен'
    )
    status = models.CharField(
        max_length=30, choices=ORDER_STATUS,
        verbose_name='Статус заказа' 
    )
    note = models.TextField(
        blank=True, verbose_name='Примечания'
    )
    transport = models.CharField(
        max_length=20, choices=TRANSPORT
    )
    transport_cost = models.DecimalField(
        max_digits=8, decimal_places=2
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ № {self.id}'

    def get_total_cost(self):
        """Метод для подсчета общей суммы товаров, включая доставку"""
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost += self.transport_cost
        return total_cost 


class OrderItem(models.Model):
    """Модель для связи продукта и его количества с конкретным заказом"""
    order = models.ForeignKey(
        Order, related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity



