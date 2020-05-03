from random import shuffle, random
from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse

from .models import Contact

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    contact_set = Contact.objects.filter(last_date__gt=now())
    contacts = sorted(contact_set, key=lambda x: random())[:6]  # shuffle query_set
    return render(request, 'main.html', context={"contacts": contacts})


def market(request):
    return render(request, 'market.html')


def services(request):
    return render(request, 'services.html')
