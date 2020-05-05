from django import template

register = template.Library()


@register.filter
def cloud_image(value):
    if value is None:
        return "https://via.placeholder.com/100x100?text=Без фото"
    return value.image.build_url(width=100, height=100, crop="thumb")

