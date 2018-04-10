from django.contrib import admin
from utils.abstract_admin import ImageAdmin
from .models import IncludeArea


@admin.register(IncludeArea)
class IncludeAreaAdmin(ImageAdmin):
    menu_title = '4.Подключаемые области'
    menu_group = 'Контент'
    search_fields = ('^title', 'code')
    #
    list_display = ('get_thumbnail_html', 'title', 'is_show', 'code', 'sort')
    list_display_links = ('get_thumbnail_html', 'title')
    list_editable = ('is_show', 'sort')
    list_filter = ('is_show', 'code')

