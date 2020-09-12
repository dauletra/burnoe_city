from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import ListView, DetailView, View
from django.db.models import Count, F

from .models import Contact, News, Event, Service, ServiceCategory, SearchQuery, Tag

import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    best_length = 7
    only_length = 7

    contacts = Contact.objects.filter(last_date__gt=now()).order_by('?')

    news = News.objects.all()[:5]

    best_adverts = Service.objects.active().filter(elect_date__gt=now()).order_by('?')[:best_length]

    services = Service.objects.active().filter(elect_date__isnull=True, only=True)[:only_length]

    if services.count() < only_length:
        minus = only_length - services.count()
        temp_services = Service.objects.active().filter(elect_date__isnull=True, only=False)[:minus]
        services = services | temp_services

    service_count = Service.objects.active().count()
    categories = ServiceCategory.objects.annotate(service_count=Count('service'))
    service_categories = categories

    return render(request, 'main.html',
                  context={
                      "contacts": contacts,
                      "news": news,
                      "best_adverts": best_adverts,
                      "services": services,
                      "service_count": service_count,
                      "service_categories": service_categories
                  })


class SearchResult(View):
    template_name = 'search_result.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        # если нет текста вернуть 20 случайных объявлении
        if query == '':
            services = Service.objects.active().order_by('?')[:20]
            other_services = []
            title = 'Поиск услуг по Жуалынскому району'
        else:
            # сохранить текст запроса в базе данных
            search_query, _ = SearchQuery.objects.get_or_create(text=query.lower())
            search_query.count=F('count')+1
            search_query.save()
            # поиск по тегу
            try:
                tag = Tag.objects.get(text=query.lower())
                services_by_tag = Service.objects.active().filter(tags=tag)
                services_out_tag = Service.objects.active().exclude(tags=tag)
                print('--- By Tags Count = {0}'.format(len(services_by_tag)))
            except Tag.DoesNotExist:
                services_by_tag = Service.objects.none()
                services_out_tag = Service.objects.active()
            # поиск по тексту
            services_by_icontains = services_out_tag.filter(content__icontains=query)
            services = services_by_tag | services_by_icontains
            if len(services) < 10:
                other_services = services_out_tag.exclude(content__icontains=query).order_by('?')[:5]
            title = 'Результаты поиска по запросу {0}'.format(query)

        return render(request, self.template_name, {'query': query, 'services': services, 'title': title, 'other_services': other_services})


def hints_json(request):
    length = 7
    q = request.GET['q']
    tags_contains = Tag.objects.filter(text__icontains=q.lower())
    tags = [tag.text for tag in tags_contains][:length]
    return JsonResponse(tags, safe=False)


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
