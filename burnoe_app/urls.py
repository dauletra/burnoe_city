from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('services', views.ServiceList.as_view(), name='service_list'),
    path('services/<int:pk>', views.ServiceDetail.as_view(), name='service_detail'),

    path('search', views.SearchResult.as_view(), name='search'),

    path('terms', views.terms, name='terms'),
    path('confident', views.confident, name='confident'),
    path('help', views.help_page, name='help'),

    path('hints.json', views.hints_json, name='hints_json'),
    path('carousel/<int:id>.html', views.carousel_html, name='carousel_html')
]