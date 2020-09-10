from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.db.models import Count

from .models import Contact, News, Event, Service, ServiceCategory

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    best_length = 7
    only_length = 7

    contacts = Contact.objects.filter(last_date__gt=now()).order_by('?')

    news = News.objects.all()[:5]

    best_adverts = Service.objects.active().filter(elect_date__gt=now()).order_by('?')[:7]

    services = Service.objects.active().filter(elect_date__isnull=True, only=True)[:only_length]

    if services.count() < only_length:
        minus = only_length - services.count()
        temp_services = Service.objects.active().filter(elect_date__isnull=True, only=False)[:minus]
        services = services | temp_services

    service_count = Service.objects.active().count()
    categories = ServiceCategory.objects.annotate(service_count=Count('service'))
    service_categories = categories
    other_service_categories = categories[9:]

    return render(request, 'main.html',
                  context={
                      "contacts": contacts,
                      "news": news,
                      # "events": events,
                      "best_adverts": best_adverts,
                      "services": services,
                      "service_count": service_count,
                      "service_categories": service_categories,
                      "other_service_categories": other_service_categories
                  })


class ServiceList(ListView):
    context_object_name = 'services'
    ordering = ['created_date']
    queryset = Service.objects.active()
    template_name = 'service_list.html'
    paginate_by = 6

    def get_queryset(self):
        try:
            cat_id = int(self.request.GET.get('category', ''))
        except ValueError:
            return super().get_queryset()
        else:
            return Service.objects.active().filter(category=cat_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        res = super().get_context_data(**kwargs)
        try:
            cat_id = int(self.request.GET.get('category', ''))
            current_category = ServiceCategory.objects.get(pk=cat_id)
        except ValueError:
            current_category = None
        res['service_categories'] = ServiceCategory.objects.annotate(service_count=Count('service'))
        res['service_count'] = self.get_queryset().count()
        res['current_category'] = current_category
        res['filter_param_str'] = '&category='+str(current_category.id) if current_category is not None else ''
        return res


class ServiceDetail(DetailView):
    template_name = 'service_detail.html'
    queryset = Service.objects.all()
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        obj = res['advert']
        res['other_adverts'] = Service.objects.active().filter(category=obj.category.id).exclude(id=obj.id).order_by('?')[:4]
        return res
