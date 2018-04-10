from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter
from utils.abstract_admin import DefaultSettings, ABSDefaultMPTTAdmin
from .models import MainMenu


@admin.register(MainMenu)
class MainMenuAdmin(ABSDefaultMPTTAdmin, DefaultSettings):
    menu_title = 'Главное меню'
    menu_group = 'Меню'

    actions = ABSDefaultMPTTAdmin.abs_actions + DefaultSettings.abs_actions
    radio_fields = {'parent': admin.VERTICAL, 'catalog': admin.VERTICAL, 'blog': admin.VERTICAL,
                    'page': admin.VERTICAL, 'gallery': admin.VERTICAL}
    search_fields = ('name', 'parent')
    list_display = ('name', 'parent', 'is_show', 'catalog', 'page', 'blog', 'gallery', 'sort')
    list_display_links = ('name', 'parent'  )
    list_editable = ('is_show', 'sort')
    fieldsets = (
        ('Основные настройки', {
            'fields': (('name', 'is_show'), 'sort', 'parent'),
        }),
        ('Каталог', {
            'fields': ('catalog',),
            'classes': ('collapse',)
        }),
        ('Блог', {
            'fields': ('blog',),
            'classes': ('collapse',)
        }),
        ('Галерея', {
            'fields': ('gallery',),
            'classes': ('collapse',)
        }),
        ('Страницы', {
            'fields': ('page',),
            'classes': ('collapse',)
        })
    )
    list_filter = (
        'is_show',
        ('catalog', TreeRelatedFieldListFilter), ('blog', TreeRelatedFieldListFilter),
        ('gallery', TreeRelatedFieldListFilter),
        'level', 'tree_id')