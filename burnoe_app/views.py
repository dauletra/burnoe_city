from random import shuffle, random
from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse

from .models import Contact, Product, ProductCategory

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    contacts = Contact.objects.filter(last_date__gt=now()).order_by('?')
    products = Product.objects.all()[:4]
    product_count = Product.objects.all().count() - 4
    product_categories = ProductCategory.objects.all()
    # contacts = sorted(contact_set, key=lambda x: random())[:6]  # shuffle query_set

    return render(request, 'main.html',
                  context={
                      "contacts": contacts,
                      "products": products,
                      "product_count": product_count,
                      "product_categories": product_categories
                  })


def market(request):
    return render(request, 'market.html')


def services(request):
    return render(request, 'services.html')
