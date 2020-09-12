from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.SearchResult.as_view(), name='search_result'),
    path('services', views.ServiceList.as_view(), name='service_list'),
    path('services/<int:pk>', views.ServiceDetail.as_view(), name='service_detail')
]