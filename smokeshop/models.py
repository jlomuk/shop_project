from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


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

    def get_absolute_url(self):
        return reverse('smokeshop:product_list_by_category', args=[self.slug])


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
                                 verbose_name='Категория',
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
    available = models.BooleanField(default=True,
                                    verbose_name='Наличие товара'
                                    )
    image = models.ImageField(upload_to='products', blank=True)

    class Meta:
        ordering = ('-name', )
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('smokeshop:product_detail',
                       args=[self.category.slug, self.slug])


class Feedback(models.Model):
    """Модель для хранения оценок и отзывов на конкретный товар"""
    product = models.ForeignKey(Product,
                                verbose_name='Продукт',
                                related_name='feedbacks',
                                on_delete=models.CASCADE)
    author = models.CharField(max_length=100, verbose_name='Автор')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    text = models.TextField(blank=True,
                            verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}-{self.rating} | {self.created}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
