from django.contrib import admin
from django.utils.timezone import now

from datetime import timedelta

from .models import (Contact, News, Event, SearchText, Tag,
                     Service, ServiceCategory, ServicePhoto)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'phone', 'created_date', 'last_date', 'is_active']
    list_display_links = ['id', 'name']
    actions = ['add_last_date']

    def add_last_date(self, request, queryset):
        queryset.update(last_date=now() + timedelta(days=21))

    add_last_date.short_description = "Увеличить дату удаления на 21 день"


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link', 'created_date']
    list_display_links = ['id', 'title']


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name1', 'name2', 'created_date', 'last_date', 'is_active']
    list_display_links = ['id', 'name1']


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order', 'count']
    list_display_links = ['id', 'name']

    def count(self, obj):
        return obj.service_set.count()


class ServicePhotoInline(admin.StackedInline):
    model = ServicePhoto
    extra = 2


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'contact', 'category_name', 'get_tags', 'photos', 'last_date', 'is_best', 'is_active']
    list_display_links = ['id', 'title']
    inlines = [ServicePhotoInline]
    actions = ['add_last_date', 'add_last_elect_date']
    filter_horizontal = ('tags',)

    def category_name(self, obj):
        return obj.category.name

    def photos(self, obj):
        return obj.servicephoto_set.count()

    def get_tags(self, obj):
        return ", ".join([str(t) for t in obj.tags.all()])

    def add_last_date(self, request, queryset):
        queryset.update(last_date=now()+timedelta(days=21))

    def add_last_elect_date(self, request, queryset):
        queryset.update(elect_date=now()+timedelta(days=14))

    add_last_date.short_description = 'Увеличить дату удаления на 21 день'
    add_last_elect_date.short_description = 'Увел. дату удал. из избран. на 14 день'
    category_name.short_description = 'Категория'
    category_name.admin_order_field = 'category__name'

    photos.short_description = 'Фото'


class SearchTextAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'count', 'modified_date']
    list_display_links = ['id', 'text']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'alternative_text', 'count', 'modified_date']
    list_display_links = ['id', 'text']


admin.site.register(Tag, TagAdmin)
admin.site.register(SearchText, SearchTextAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Service, ServiceAdmin)
