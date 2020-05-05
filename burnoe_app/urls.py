from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market', views.ProductList.as_view(), name='products'),
    path('services', views.ServiceList.as_view(), name='services')
]