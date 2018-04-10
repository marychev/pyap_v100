# -*- encoding: utf-8 -*-
from django.template.defaultfilters import stringfilter
from django.template import TemplateSyntaxError
from django import template

register = template.Library()


@register.filter(is_safe=False)
@stringfilter
def rupluralize(value, arg):
    # pluralize for russian language  {{someval|rupluralize:"товар,товара,товаров"}}
    bits = arg.split(',')
    try:
        value = str(0 if not value or int(value) <= 0 else value)[-1:]  # patched version
        return bits[0 if value == '1' else (1 if value in '234' else 2)]
    except:
        raise TemplateSyntaxError

