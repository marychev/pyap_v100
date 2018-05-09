from django.contrib import admin
from utils.abstract_admin import ImageAdmin, ImageInlineTabularAdmin, SEOAdmin
from .models import Home, HomeImage


# INLINE ---

class HomeImageInline(ImageInlineTabularAdmin):
    model = HomeImage

# --------------------------------------------


@admin.register(Home)
class HomeAdmin(ImageAdmin, SEOAdmin):
    menu_title = 'Главная страница'
    menu_group = 'Контент'

    inlines = (HomeImageInline,)
    raw_id_fields = ('blog',)
    readonly_fields = ('get_image_thumb',)

    search_fields = ('title',)
    list_filter = ('is_show', 'blog')
    list_display = ('get_image_thumb', 'title', 'get_html', 'is_show')
    list_display_links = ('get_image_thumb', 'title',)
    list_editable = ('is_show',)
    fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {
            'fields': (
                'get_image_thumb', ('title', 'is_show'),
                'html', 'blog',
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
