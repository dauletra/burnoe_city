from django import template

register = template.Library()


@register.filter
def cloud_image(value):
    return value.build_url(width=100, height=100, crop="thumb")

