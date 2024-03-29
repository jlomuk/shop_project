# Generated by Django 3.2.5 on 2021-07-30 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('smokeshop', '0005_auto_20210730_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.CharField(max_length=250, verbose_name='Адрес')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Индекс')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('Created', 'Создан'), ('Processing', 'В обработке'), ('Shipped', 'Отправлен'), ('Ready pickup', 'Готов к выдачи'), ('Completed', 'Завершен')], max_length=30, verbose_name='Статус заказа')),
                ('note', models.TextField(blank=True, verbose_name='Примечания')),
                ('transport', models.CharField(choices=[('Courier', 'Курьер'), ('pickup', 'Самовывоз')], max_length=20)),
                ('transport_cost', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='smokeshop.product')),
            ],
        ),
    ]
