from django.contrib import admin

from .models import (Contact, News,
                     Service, ServiceCategory, ServicePhoto,
                     Product, ProductCategory, ProductPhoto)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'phone', 'created_date', 'last_date', 'is_active']
    list_display_links = ['id', 'name']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link', 'created_date']
    list_display_links = ['id', 'title']


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order']


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order']


class ServicePhotoInline(admin.StackedInline):
    model = ServicePhoto
    extra = 2


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'contact', 'content', 'category_name', 'photos', 'created_date']
    list_display_links = ['id', 'title']
    inlines = [ServicePhotoInline]

    def category_name(self, obj):
        return obj.category.name

    def photos(self, obj):
        return obj.servicephoto_set.count()

    category_name.short_description = 'Категория'
    category_name.admin_order_field = 'category__name'

    photos.short_description = 'Фото'


class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'category_name', 'photos', 'created_date']
    list_display_links = ['id', 'title']
    inlines = [ProductPhotoInline]

    def category_name(self, obj):
        return obj.category.name

    def photos(self, obj):
        return obj.productphoto_set.count()

    category_name.short_description = 'Категория'
    category_name.admin_order_field = 'category__name'

    photos.short_description = 'Фото'


admin.site.register(Contact, ContactAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
