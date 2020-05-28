from django import template

register = template.Library()


@register.filter
def crop_image(photo_entity, args):
    if args is None:
        return False
    width, height = [int(arg) for arg in args.split(',')]
    if photo_entity is None:
        return f'https://via.placeholder.com/{width}x{height}?text=Без фото'
    return photo_entity.image.build_url(width=width, height=height, crop="thumb")
