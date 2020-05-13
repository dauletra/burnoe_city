from django import template

register = template.Library()


@register.filter
def event_photo(cloud_field):
    if cloud_field is None:
        return "https://via.placeholder.com/80x80?text=Без фото"
    return cloud_field.build_url(width=80, height=80, crop="thumb")

