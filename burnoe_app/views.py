from django.shortcuts import render
from django.http import HttpResponse

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    return render(request, 'main.html')

def market(request):
    return render(request, 'market.html')

def services(request):
    return render(request, 'services.html')
