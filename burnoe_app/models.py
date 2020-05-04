from django.db import models
from django.utils.timezone import now
from cloudinary.models import CloudinaryField

from datetime import timedelta
# todo remove images from cloudinary when object deleted


def after():
    return now() + timedelta(days=7)


def after_advert():
    return now() + timedelta(days=21)


class Contact(models.Model):
    name = models.CharField(max_length=17, verbose_name='Название')
    price = models.CharField(max_length=17, verbose_name='Цена')
    phone = models.CharField(max_length=17, verbose_name='Телефон')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    last_date = models.DateTimeField(verbose_name="Дата удаления", default=after)

    def is_active(self):
        return self.last_date > now()

    is_active.boolean = True

    def __str__(self):
        return self.name or self.id


# ---- ----

class Category(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField(verbose_name='Порядок', default=10)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['order']


class ServiceCategory(Category):
    class Meta(Category.Meta):
        verbose_name_plural = 'Service categories'


class ProductCategory(Category):
    class Meta(Category.Meta):
        verbose_name_plural = 'Product categories'


# ---- ----

class Advert(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    last_date = models.DateTimeField(verbose_name='Дата удаления', default=after_advert)

    def is_active(self):
        return self.last_date > now()

    is_active.boolean = True

    def __str__(self):
        return self.title or self.id

    class Meta:
        abstract = True
        ordering = ['-created_date']


# ----

class Service(Advert):
    contact = models.CharField(max_length=100, verbose_name='Телефон и адрес')
    category = models.ForeignKey(to=ServiceCategory, on_delete=models.PROTECT, verbose_name='Категория')

    class Meta(Advert.Meta):
        pass


class ServicePhoto(models.Model):
    image = CloudinaryField('image')
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)


# ----

class Product(Advert):
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    class Meta(Advert.Meta):
        pass


class ProductPhoto(models.Model):
    image = CloudinaryField('image')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
