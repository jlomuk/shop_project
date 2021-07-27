# Generated by Django 3.2.5 on 2021-07-26 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smokeshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-name',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='awailable',
            new_name='available',
        ),
        migrations.AlterField(
            model_name='product',
            name='is_nicotine',
            field=models.BooleanField(default=True, verbose_name='Присутствие никотина'),
        ),
    ]