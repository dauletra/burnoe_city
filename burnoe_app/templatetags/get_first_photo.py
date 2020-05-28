from django import template

register = template.Library()


@register.filter
def get_first_photo(advert: 'Service'):
    return advert.__getattribute__('servicephoto_set').first()
