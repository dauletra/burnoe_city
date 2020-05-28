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


class News(models.Model):
    title = models.CharField(max_length=70, verbose_name='Заголовок')
    link = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-created_date']

# ---- ----


class Event(models.Model):
    name1 = models.CharField(max_length=20, verbose_name='Заголовок 1')
    name2 = models.CharField(max_length=20, verbose_name='Заголовок 2')
    last_date = models.DateTimeField(verbose_name='Дата событии')
    photo = CloudinaryField('image', null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def is_active(self):
        return self.last_date > now()

    is_active.boolean = True

    def __str__(self):
        return self.name1

    class Meta:
        ordering = ['last_date']

# ---- -----


class ServiceCategory(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField(verbose_name='Порядок', default=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Service categories'


class ServiceManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(last_date__gt=now())


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    last_date = models.DateTimeField(verbose_name='Дата удаления', default=after_advert)

    contact = models.CharField(max_length=100, verbose_name='Телефон и адрес')
    category = models.ForeignKey(to=ServiceCategory, on_delete=models.PROTECT, verbose_name='Категория')

    objects = ServiceManager()

    def is_active(self):
        return self.last_date > now()

    is_active.boolean = True

    def __str__(self):
        return self.title or self.id

    class Meta:
        ordering = ['-created_date']


class ServicePhoto(models.Model):
    image = CloudinaryField('image')
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)
