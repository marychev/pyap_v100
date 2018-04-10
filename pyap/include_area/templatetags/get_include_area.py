from django import template
from django.template.loader import render_to_string
from django.conf import settings
from include_area.models import IncludeArea
from htmlmin.minify import html_minify


register = template.Library()


@register.simple_tag
def get_include_area(request, code, *args, **kwargs):
    """
    Примененние: {% get_include_area request code='advantages' %}
    ``````````````````````````````````````````````````````````````
    :param code: Название, уникальный код для определения типа ПО ``advantages``
        Такое же название имеет шаблон этой ПО ``advantages.html`` (+.html)
    :return: HTML шаблон, заполненный данными из QuerySet
    """
    theme_templates = settings.TEMPLATES[0]['DIRS'][0]
    file_path = '{}/include_area/templates/{}.{}'.format(theme_templates, code, 'html')
    try:
        include_areas = IncludeArea.objects.filter(code=code, is_show=True)
        html = render_to_string(file_path, {'include_areas': include_areas})
        # html = render_to_string(code + '.html', {'include_areas': include_areas})
        return html
    except IncludeArea.DoesNotExist:
        return None

