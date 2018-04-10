from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter
from utils.abstract_admin import ImageAdmin, ImageInlineTabularAdmin, SEOAdmin, ABSDefaultMPTTAdmin
from .models import Catalog, CatalogImage


# INLINE ---

class CatalogImageInline(ImageInlineTabularAdmin):
    model = CatalogImage

# --------------------------------------------


@admin.register(Catalog)
class CatalogAdmin(ABSDefaultMPTTAdmin, ImageAdmin, SEOAdmin):
    menu_title = "1.Каталог"
    menu_group = "Каталог"

    actions = ABSDefaultMPTTAdmin.abs_actions
    inlines = (CatalogImageInline,)
    raw_id_fields = ('parent',)
    readonly_fields = ('get_image_thumb', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}
    # radio_fields = {'parent': admin.VERTICAL}

    search_fields = ('title', 'parent__title')
    list_filter = (
        'is_show',
        ('parent', TreeRelatedFieldListFilter)
    )
    list_display = ('title', 'get_image_thumb', 'parent', 'sort', 'is_show')
    list_display_links = ('title', 'get_image_thumb')
    list_editable = ('parent', 'sort', 'is_show')

    fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {
            'fields': (
                'get_image_thumb', ('title', 'is_show'), 'description', 'parent', 'html', 'sort',
            ),
        }),
        ('СЕО-НАСТРОЙКИ', {
            'classes': ('collapse',),
            'fields': SEOAdmin.abs_fields,
        }),
        ('ИНФОРМАНЦИЯ', {
            'classes': ('collapse',),
            'fields': readonly_fields,
        }),
    )

    # TODO: create this method!
    # actions = ('clone_object',)
    #
    # def clone_object(self, request, queryset):
    #     """Копирование(клонирование) выбранных объектов - action"""
    #     for obj in queryset:
    #         obj.title += '_CLONE'
    #         obj.slug += '_CLONE'
    #         obj.html += '_CLONE'
    #         obj.id = None
    #         obj.save()
    # clone_object.short_description = 'Клонировать'

# @admin.register(Catalog)
# class CatalogAdmin(DraggableMPTTAdmin, ImageAdmin):
#     menu_title = "Категории"
#     menu_group = "Каталог товаров"
#     radio_fields = {'parent': admin.VERTICAL}
#     prepopulated_fields = {'url': ('name',)}
#     search_fields = ('^title', '^parent__title')
#     fields = (('name', 'is_show'),
#               'parent', 'description',  ('get_thumbnail_html', 'image'),
#               'url', 'seo_title', 'seo_description', 'seo_keywords')
#     list_display = ('tree_actions', 'indented_title', 'get_thumbnail_html', 'url', 'is_show')
#     list_editable = ('is_show',)
#     list_filter = ('is_show',)  # 'level', 'tree_id')
