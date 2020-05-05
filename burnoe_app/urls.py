from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market', views.market, name='products'),
    path('services', views.services, name='services')
]