from django.db import models


class Category(models.Model):
    """
    Модель содержит информацию 
    по табакам разного вида(кальяный, для трубок и тд..)
    """
    name = models.CharField(max_length=75,
                verbose_name='Вид табака',
                unique=True, 
    )
    slug = models.SlugField(max_length=75, unique=True)

    class Meta:
        ordering = ('-name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель содержит характеристики конкретного продукта"""
    RATING = (
        ('1', 'Очень низкая'),
        ('2', 'Низкая'),
        ('3', 'Средняя'),
        ('4', 'Высокая'),
        ('5', 'Очень высокая')
    )

    category = models.ForeignKey(Category,
                related_name='products',
                on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150,
                verbose_name='Название продукта',
                unique=True,
    )
    slug = models.SlugField(max_length=100, unique=True)
    is_nicotine = models.BooleanField(default=True, 
                verbose_name='Присутствие никотина')
    brand = models.CharField(max_length=75, 
                verbose_name='Бренд')
    maker_country = models.CharField(max_length=100,
                verbose_name='Страна производитель')
    description = models.TextField()
    weight = models.PositiveIntegerField(
                verbose_name='Вес'
    )
    strength = models.CharField(choices=RATING,
                max_length=100,
                verbose_name='Крепкость',
    )
    smoking = models.CharField(choices=RATING,
                max_length=100,
                verbose_name='Дымность',
    )
    taste = models.CharField(max_length=100,
                verbose_name='Вкус',
    ) 
    price = models.DecimalField(max_digits=8, 
                decimal_places=2, 
                verbose_name='Цена')
    awailable = models.BooleanField(default=True,
                verbose_name='Наличие товара'
    )
    image = models.ImageField(upload_to='products')

    class Meta:
        ordering = ('-name', )
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

