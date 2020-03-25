from django.contrib import admin

from .models import (Contact,
                     Restaurant, Row, PhotoRestaurant,
                     Service, PhotoService, CategoryService)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'phone', 'created_date', 'modified_date']
    list_display_links = ['id', 'name']


class RowInline(admin.StackedInline):
    model = Row
    extra = 3


class PhotoRestaurantInline(admin.StackedInline):
    model = PhotoRestaurant
    extra = 2


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'photos', 'rows', 'created_date', 'modified_date']
    list_display_links = ['id', 'name']
    inlines = [RowInline, PhotoRestaurantInline]

    def photos(self, obj):
        return obj.photorestaurant_set.count()

    def rows(self, obj):
        return obj.row_set.count()

    photos.short_description = 'Фото'
    rows.short_description = 'Пункты'


class PhotoServiceInline(admin.StackedInline):
    model = PhotoService
    extra = 2


class CategoryServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'contact', 'content', 'category_name', 'photos', 'created_date']
    list_display_links = ['id', 'title']
    inlines = [PhotoServiceInline]

    def category_name(self, obj):
        return obj.category.name

    def photos(self, obj):
        return obj.photoservice_set.count()

    category_name.short_description = 'Категория'
    category_name.admin_order_field = 'category__name'

    photos.short_description = 'Фото'


admin.site.register(Contact, ContactAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(CategoryService, CategoryServiceAdmin)
