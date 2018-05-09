from django.contrib import admin
from django.db import models
from django.forms import TextInput
from utils.abstract_admin import ImageAdmin
from .models import SliderHome


@admin.register(SliderHome)
class SliderHomeAdmin(ImageAdmin):
    menu_title = 'Слайдер'
    menu_group = 'Контент'

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '60'})},
    }

    search_fields = ('title',)
    list_display = ('get_thumbnail_html', 'title', 'description', 'url', 'sort')
    list_display_links = ('get_thumbnail_html', 'title')
    list_editable = ('sort',)
    list_filter = ('title', )

    fields = ('title', 'image', 'description', 'url', 'sort')
