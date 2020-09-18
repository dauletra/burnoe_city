from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import ListView, DetailView, View
from django.db.models import Count, F

from django.contrib.postgres.search import SearchQuery, SearchVector

from .models import MomentAdvert, News, Service, ServiceCategory, ServicePhoto, SearchText, Tag
import time
import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    best_length = 7
    monopolists_length = 7

    contacts = MomentAdvert.objects.filter(last_date__gt=now()).order_by('?')

    news = News.objects.all()[:5]

    best_adverts = Service.objects.active().filter(last_best_date__gt=now()).order_by('?')[:best_length]

    services = Service.objects.active().filter(last_best_date__isnull=True, is_monopolist=True)[:monopolists_length]

    if services.count() < monopolists_length:
        minus = monopolists_length - services.count()
        temp_services = Service.objects.active().filter(last_best_date__isnull=True, is_monopolist=False)[:minus]
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
        # start_time = time.time()
        query: str = request.GET.get('query', '')
        # если нет текста вернуть 20 случайных объявлении
        other_services = []
        if query == '':
            services = Service.objects.active().order_by('?')[:20]
            title = 'Поиск услуг - рекламно-информационный сайт Жуалынского района'
        else:
            # сохранить текст запроса в базе данных
            client_query, _ = SearchText.objects.get_or_create(text=query.lower())
            client_query.count=F('count')+1
            client_query.save()
            # поиск по тегу
            try:
                tag = Tag.objects.get(text=query.lower())
                services_by_tag = Service.objects.active().filter(tags=tag)
            except Tag.DoesNotExist:
                services_by_tag = Service.objects.none()
            # поиск по полному тексту
            search_vector = SearchVector('title', 'content', config='russian')
            search_query = SearchQuery(query, config='russian')
            services_by_query = Service.objects.active().annotate(search=search_vector).filter(search=search_query)

            services = services_by_tag | services_by_query
            if len(services) < 10:
                other_services = Service.objects.active().exclude(content__icontains=query).order_by('?')[:5]
            title = 'Результаты поиска по запросу {0}'.format(query)
        # print('@Timer: {0}'.format(time.time()-start_time))
        return render(request, self.template_name, {'query': query, 'services': services.distinct(), 'title': title, 'other_services': other_services})


def hints_json(request):
    length = 7
    q = request.GET['q']
    tags_contains = Tag.objects.filter(text__icontains=q.lower())
    tags = [tag.text for tag in tags_contains][:length]
    return JsonResponse(tags, safe=False)


def carousel_html(request, id):
    try:
        advert = Service.objects.active().get(id=id)
    except Service.DoesNotExist:
        advert = None
    return render(request, '_carousel.html', context={'advert': advert})


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
    queryset = Service.objects.active()
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        obj = res['advert']
        res['other_adverts'] = Service.objects.active().filter(category=obj.category.id).exclude(id=obj.id).order_by('?')[:5]
        return res


def terms(request):
    return render(request, "terms.html", {})


def confident(request):
    return render(request, "confident.html", {})


def help_page(request):
    return render(request, "help.html", {})
