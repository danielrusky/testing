from django import template

from config.settings import MEDIA_URL

register = template.Library()


@register.filter()
def media_tag(product):
    if product:
        return f'/media/{product}'
    return ''


@register.simple_tag()
def media_tag(product):
    if product:
        return MEDIA_URL + str(product)
    return ''

