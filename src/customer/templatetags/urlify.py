from urllib.parse import quote_plus
from django import template

register = template.Library()


@register.filter
def urlify(value):
    print('value before:', value)
    value = quote_plus(value)
    print('value after:', value)
    return value

