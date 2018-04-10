from django import template
register = template.Library()


@register.filter
def url_handler(obj, name='catalog'):
    """определить тип объекта и его УРЛ - (Catalog|)"""
    if 'catalog' in name:
        return obj.get_absolute_url()
    if 'mainmenu' in name:
        if obj.blog:
            return obj.blog.get_absolute_url()
        if obj.page:
            return obj.page.get_absolute_url()
        if obj.catalog:
            return obj.catalog.get_absolute_url()
        if obj.gallery:
            return obj.gallery.get_absolute_url()
        return '/'
    return '/'
