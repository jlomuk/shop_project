from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Модель для хранения профиля покупателя"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=30,
        blank=True,
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=250,
        blank=True,
    )
    postal_code = models.CharField(
        verbose_name='Почтовый индекс',
        max_length=30,
        blank=True,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'

    def __str__(self):
        return f'{self.user.username} профиль'

