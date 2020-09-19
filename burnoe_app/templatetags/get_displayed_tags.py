from django import template

register = template.Library()


@register.filter
def get_displayed_tags(tags):
    return tags.filter(is_displayed=True)