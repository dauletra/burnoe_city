from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.SearchResult.as_view(), name='search_result'),
    path('hints.json', views.hints_json, name='hints_json'),
    path('carousel/<int:id>.html', views.carousel_html, name='carousel_html'),
    path('services', views.ServiceList.as_view(), name='service_list'),
    path('services/<int:pk>', views.ServiceDetail.as_view(), name='service_detail')
]