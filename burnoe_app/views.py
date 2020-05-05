from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Contact, Product, ProductCategory, Service, ServiceCategory

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    contacts = Contact.objects.filter(last_date__gt=now()).order_by('?')

    products = Product.objects.all()[:4]
    product_count = Product.objects.all().count()
    product_categories = ProductCategory.objects.all()

    services = Service.objects.all()[:4]
    service_count = Service.objects.all().count()
    service_categories = ServiceCategory.objects.all()
    # contacts = sorted(contact_set, key=lambda x: random())[:6]  # shuffle query_set

    return render(request, 'main.html',
                  context={
                      "contacts": contacts,
                      "products": products,
                      "product_count": product_count,
                      "product_categories": product_categories,
                      "services": services,
                      "service_count": service_count,
                      "service_categories": service_categories
                  })


class ProductList(ListView):
    context_object_name = 'products'
    queryset = Product.objects.filter(last_date__gt=now())
    template_name = 'market_list.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        res = super().get_context_data(**kwargs)
        res['product_categories'] = ProductCategory.objects.all()
        res['product_count'] = Product.objects.filter(last_date__gt=now()).count()
        return res


class ProductDetail(DetailView):
    template_name = 'advert_detail.html'
    queryset = Product.objects.filter(last_date__gt=now())
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        obj = Product.objects.get(pk=self.kwargs.get('pk'))
        res['photos'] = obj.productphoto_set.all()
        res['other_adverts'] = Product.objects.filter(last_date__gt=now(), category=obj.category.id).exclude(id=obj.id)[:4]
        res['name'] = 'product'
        return res


class ServiceList(ListView):
    context_object_name = 'services'
    queryset = Service.objects.filter(last_date__gt=now())
    template_name = 'service_list.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        res = super().get_context_data(**kwargs)
        res['service_categories'] = ServiceCategory.objects.all()
        res['service_count'] = Service.objects.filter(last_date__gt=now()).count()
        return res


class ServiceDetail(DetailView):
    template_name = 'advert_detail.html'
    queryset = Service.objects.filter(last_date__gt=now())
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        obj = Service.objects.get(pk=self.kwargs.get('pk'))
        res['photos'] = obj.servicephoto_set.all()
        res['other_adverts'] = Service.objects.filter(last_date__gt=now(), category=obj.category.id).exclude(id=obj.id)[:4]
        res['name'] = 'service'
        return res