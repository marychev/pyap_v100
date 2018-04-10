from django.contrib import admin
from mptt.admin import TreeRelatedFieldListFilter
from utils.abstract_admin import ABSDefaultMPTTAdmin, ImageAdmin, ImageInlineTabularAdmin, SEOAdmin
from .models import Gallery, GalleryImage


# INLINE ---

class GalleryImageInline(ImageInlineTabularAdmin):
    model = GalleryImage

# ==============================


@admin.register(Gallery)
class GalleryAdmin(ABSDefaultMPTTAdmin, ImageAdmin, SEOAdmin):
    menu_title = "1.Галерея"
    menu_group = "Галерея"
    actions = ABSDefaultMPTTAdmin.abs_actions + ImageAdmin.abs_actions + SEOAdmin.abs_actions
    inlines = (GalleryImageInline,)
    raw_id_fields = ('parent',)
    readonly_fields = ('get_image_thumb', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}
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
                'get_image_thumb', ('title', 'is_show'), 'parent', 'html'
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

    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('get_image_thumb', )  # 'created', 'updated')
    # raw_id_fields = ('parent',)
    # date_hierarchy = 'created'
    # search_fields = ('title', 'seo_title')
    # list_filter = (
    #     'is_show', 'parent',
    #     ('created', DateRangeFilter), ('updated', DateRangeFilter))
    # list_display = ('title', 'get_image_thumb', 'parent', 'is_show')
    # list_display_links = ('title', 'get_image_thumb')
    # list_editable = ('parent', 'is_show')
    # fieldsets = (
    #     ('ОСНОВНЫЕ ДАННЫЕ', {
    #         'fields': (
    #             ('title', 'is_show'),
    #             'parent', 'description', 'html', 'sort',
    #             'created', 'updated'
    #         )
    #     }),
    #     ('SEO НАСТРОЙКИ', {
    #         'fields': SEOAdmin._fields,
    #         'classes': ('collapse',)
    #     }),
    #     ('ИНФОРМАНЦИЯ', {
    #         'classes': ('collapse',),
    #         'fields': readonly_fields,
    #     }),
    # )


@admin.register(GalleryImage)
class GalleryImageAdmin(ImageAdmin):
    menu_title = "1.Галерея: Фото"
    menu_group = "Галерея"
    raw_id_fields = ('gallery',)
    search_fields = ('image_title', 'gallery__title')
    list_filter = ('image_is_main', 'gallery')
    list_display = ('get_thumbnail_html', 'gallery', 'image_title', 'image_description', 'image_is_main')
    list_editable = ('image_title', 'image_is_main')
    list_display_links = ('get_thumbnail_html', 'gallery')
    fields = (
        ('image', 'image_is_main'),
        'gallery', 'image_title', 'image_description')
