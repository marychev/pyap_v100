from django.contrib import admin
from mptt.admin import TreeRelatedFieldListFilter
from settings_template.models import Footer, SettingsTemplate
from utils.abstract_admin import DefaultSettings, ImageAdmin
from site_info.models import SocialNetwork

from django.contrib.sites.models import Site

admin.site.unregister(Site)


@admin.register(Site)
class SiteAdmin(DefaultSettings):
    menu_title = '7.Домен'
    menu_group = 'Настройки'
    search_fields = ('name', 'domain')
    list_display = ('domain', 'name')
    list_filter = ('domain',)


@admin.register(Footer)
class FooterAdmin(DefaultSettings):
    menu_title = '2.Футер'
    menu_group = 'Настройки'
    radio_fields = {'text_info': admin.VERTICAL}
    filter_horizontal = ('list_link', 'catalog', 'page', 'blogs', 'galleries')
    search_fields = ('title',)
    list_display = ('title', 'is_show', 'text_info')
    list_editable = ('is_show',)
    list_filter = (
        'is_show', 'list_link', 'text_info', 'page',
        ('catalog', TreeRelatedFieldListFilter))
    fieldsets = (
        (None, {
            'fields': (('title', 'is_show'), 'catalog', 'page', 'galleries', 'blogs')
        }),
        ('Вариант отображения', {
            'classes': ('wide', ),
            'fields': ('text_info', 'list_link'),
        }),
    )


@admin.register(SocialNetwork)
class SocialNetworkAdmin(ImageAdmin):
    menu_title = '3.Соц.сети'
    menu_group = 'Настройки'
    search_fields = ('title', 'image_title')
    list_display = ('get_thumbnail_html', 'title', 'html_link', 'url')
    list_display_links = ('get_thumbnail_html', 'title')
    list_filter = ('image_is_main', 'title')
    fields = ('image', 'url', 'title', 'html_link')


@admin.register(SettingsTemplate)
class SettingsTemplateAdmin(DefaultSettings):
    menu_title = '1.Настройка шаблона'
    menu_group = 'Настройки'
    # filter_horizontal = ('footer',)
    search_fields = ('title',)
    fields = (
        'site',
        ('title', 'is_included'),
        'logo', 'phone', 'address',
        'home', 'footer', 'terms_of_use',
        'robots_txt', 'scripts')
    list_display = ('title', 'logo', 'phone', 'address', 'is_included')
    list_display_links = ('title', 'address')
    list_editable = ('logo', 'phone', 'is_included')
    list_filter = ('is_included', 'home', 'footer')
