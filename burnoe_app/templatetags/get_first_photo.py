from django import template

register = template.Library()


@register.filter
def get_first_photo(advert, name):
    return advert.__getattribute__(name+'photo_set').first()