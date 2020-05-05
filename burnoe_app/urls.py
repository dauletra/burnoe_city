from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market', views.ProductList.as_view(), name='product_list'),
    path('market/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('services', views.ServiceList.as_view(), name='service_list'),
    path('services/<int:pk>', views.ServiceDetail.as_view(), name='service_detail')
]