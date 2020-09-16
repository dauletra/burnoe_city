from django import template

register = template.Library()


@register.filter
def pad_image(photo, args):
    if args is None:
        return False
    width, height = [int(arg) for arg in args.split(',')]
    if photo is None:
        return f'https://via.placeholder.com/{width}x{height}?text=Без фото'
    return photo.image.build_url(width=width, height=height, crop='fit')