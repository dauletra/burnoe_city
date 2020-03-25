from django.db import models
from cloudinary.models import CloudinaryField

# todo remove images from cloudinary when object deleted


class Contact(models.Model):
    name = models.CharField(max_length=17, verbose_name='Название')
    price = models.CharField(max_length=17, verbose_name='Цена')
    phone = models.CharField(max_length=17, verbose_name='Телефон')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name or self.id


class Restaurant(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or self.id


class Row(models.Model):
    name = models.CharField(max_length=10, blank=True)
    value = models.CharField(max_length=50, verbose_name='Короткое описание')
    order = models.IntegerField(verbose_name='Порядок', default=10)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']


class PhotoRestaurant(models.Model):
    image = CloudinaryField('image')
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)


class CategoryService(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField(verbose_name='Порядок', default=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    contact = models.CharField(max_length=100, verbose_name='Телефон и адрес')
    content = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(to=CategoryService, on_delete=models.PROTECT, verbose_name='Категория')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title or self.id


class PhotoService(models.Model):
    image = CloudinaryField('image')
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
