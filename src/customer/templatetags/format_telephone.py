from django import template

register = template.Library()


@register.filter
def format_telephone(value):
    if len(value) == 10:
        value = "({}) {}-{}".format(value[:3], value[3:6], value[6:])
    return value

