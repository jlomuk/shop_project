# Generated by Django 3.2.5 on 2021-08-05 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smokeshop', '0005_auto_20210730_0853'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Товар в заказ', 'verbose_name_plural': 'Товары в заказе'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Created', 'Создан'), ('Processing', 'В обработке'), ('Shipped', 'Отправлен'), ('Ready pickup', 'Готов к выдачи'), ('Completed', 'Завершен')], default='Created', max_length=30, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='transport',
            field=models.CharField(choices=[('Courier', 'Курьер'), ('pickup', 'Самовывоз')], max_length=20, verbose_name='Способ получения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='transport_cost',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена доставки'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='smokeshop.product', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='Количество'),
        ),
    ]
