# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='filtro_string')
def filtro_string(dictionary, key):
    return dictionary.get(key, '')
