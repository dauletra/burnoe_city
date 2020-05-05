from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse

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


def market(request):
    products = Product.objects.all()[:10]
    product_count = Product.objects.all().count()
    product_categories = ProductCategory.objects.all()
    return render(request, 'market.html',
                  context={
                      "products": products,
                      "product_categories": product_categories,
                      "product_count": product_count
                  })


def services(request):
    services = Service.objects.all()[:10]
    service_count = Service.objects.all().count()
    service_categories = ServiceCategory.objects.all()
    return render(request, 'services.html',
                  context={
                      "services": services,
                      "service_categories": service_categories,
                      "service_count": service_count
                  })
