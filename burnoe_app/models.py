from django.db import models
from django.utils.timezone import now
from cloudinary.models import CloudinaryField

from datetime import timedelta
# todo remove images from cloudinary when object deleted


def after():
    return now() + timedelta(days=7)


def after_advert():
    return now() + timedelta(days=21)


class MomentAdvert(models.Model):
    name = models.CharField(max_length=21, verbose_name='Название')
    price = models.CharField(max_length=21, verbose_name='Цена')
    phone = models.CharField(max_length=21, verbose_name='Телефон')
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
    link = models.URLField()
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


class SearchText(models.Model):
    text = models.CharField(max_length=100, verbose_name='Запрос', unique_for_date='created_date')
    count = models.IntegerField(default=0, verbose_name='Количество запросов')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.text + ' ({0})'.format(self.count)

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = 'Search Texts'


class ServiceCategory(models.Model):
    name = models.CharField(max_length=25)
    order = models.IntegerField(verbose_name='Порядок', default=10)
    icon_name = models.CharField(max_length=100, default='default_icon.svg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Service categories'


class Tag(models.Model):
    text = models.CharField(max_length=60, verbose_name='Тег', unique=True)
    is_displayed = models.BooleanField(verbose_name='Показать?', default=False)
    alternative_text = models.TextField(verbose_name='Похожие', blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, blank=True, null=True)

    count = models.IntegerField(default=0, verbose_name='Количество запросов')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    is_displayed.boolean = True

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['category']


class ServiceManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(last_date__gt=now())


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(max_length=310, verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    last_date = models.DateTimeField(verbose_name='Дата удаления', default=after_advert)

    tags = models.ManyToManyField(Tag)

    address = models.CharField(max_length=100, verbose_name='Адрес', default='', blank=True, null=True)
    category = models.ForeignKey(to=ServiceCategory, on_delete=models.PROTECT, verbose_name='Категория')

    is_monopolist = models.BooleanField(verbose_name='Единственный в районе', default=False)
    last_best_date = models.DateTimeField(verbose_name='Избранный до', null=True, blank=True, default=None)

    is_monopolist.boolean = True

    objects = ServiceManager()

    def is_active(self):
        return self.last_date > now()

    def is_best(self):
        if self.last_best_date is None:
            return False
        return self.last_best_date > now()

    is_active.boolean = True
    is_best.boolean = True

    def __str__(self):
        return self.title or self.id

    class Meta:
        ordering = ['-created_date']


class ContactType(models.Model):
    name = models.CharField(max_length=30)
    link_suff = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    account = models.CharField(max_length=50)
    type = models.ForeignKey(to=ContactType, on_delete=models.PROTECT)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.account


class ServicePhoto(models.Model):
    image = CloudinaryField('image')
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)

