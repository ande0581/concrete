from urllib.parse import quote_plus
from django import template

register = template.Library()

@register.filter
def urlify(value):
    value = quote_plus(value)
    return value

