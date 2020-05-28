from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Contact, News, Event, Service, ServiceCategory

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    contacts = Contact.objects.filter(last_date__gt=now()).order_by('?')

    news = News.objects.all()[:5]

    events = Event.objects.all()

    best_adverts = Service.objects.active().order_by('?')[:7]

    services = Service.objects.active()[:8]
    service_count = Service.objects.active().count()
    service_categories = ServiceCategory.objects.all()

    return render(request, 'main.html',
                  context={
                      "contacts": contacts,
                      "news": news,
                      "events": events,
                      "best_adverts": best_adverts,
                      "services": services,
                      "service_count": service_count,
                      "service_categories": service_categories
                  })


class ServiceList(ListView):
    context_object_name = 'services'
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
        res['service_categories'] = ServiceCategory.objects.all()
        res['service_count'] = self.get_queryset().count()
        res['current_category'] = current_category
        res['filter_param_str'] = '&category='+str(current_category.id) if current_category is not None else ''
        return res


class ServiceDetail(DetailView):
    template_name = 'advert_detail.html'
    queryset = Service.objects.active()
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        obj = Service.objects.get(pk=self.kwargs.get('pk'))
        res['photos'] = obj.servicephoto_set.all()
        res['other_adverts'] = Service.objects.active().filter(category=obj.category.id).exclude(id=obj.id).order_by('?')[:4]
        res['name'] = 'service'
        return res