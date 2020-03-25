from django.shortcuts import render
from django.http import HttpResponse

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    return render(request, 'home.html')

