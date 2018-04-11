from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from utils.abstract_admin import ABSContentSeoAdmin, ImageInlineTabularAdmin, ImageAdmin, DefaultSettings
from .models import Page, PageImage, PageComment


# INLINE ---

class PageImageInline(ImageInlineTabularAdmin):
    model = PageImage

# --------------------------------------------


@admin.register(Page)
class PageAdmin(ABSContentSeoAdmin):
    menu_title = '2.Страницы'
    menu_group = 'Контент'
    inlines = (PageImageInline,)
    actions = ABSContentSeoAdmin.abs_actions
    raw_id_fields = ABSContentSeoAdmin.abs_raw_id_fields
    filter_horizontal = ('tags',)
    readonly_fields = ABSContentSeoAdmin.abs_readonly_fields
    search_fields = ABSContentSeoAdmin.abs_search_fields
    list_filter = ABSContentSeoAdmin.abs_list_filter
    list_display = ABSContentSeoAdmin.abs_list_display
    list_display_links = ABSContentSeoAdmin.abs_list_display_links
    list_editable = ABSContentSeoAdmin.abs_list_editable
    fieldsets = ABSContentSeoAdmin.abs_fieldsets


@admin.register(PageImage)
class PageImageAdmin(ImageAdmin):
    menu_title = "2.Страницы: Фото"
    menu_group = "Контент"
    raw_id_fields = ('page',)
    search_fields = ('image_title', 'page__title')
    list_filter = ('image_is_main', 'page')
    list_display = ('get_thumbnail_html', 'page', 'image_title', 'image_description', 'image_is_main')
    list_editable = ('image_title', 'image_is_main')
    list_display_links = ('get_thumbnail_html', 'page')
    fields = (
        ('image', 'image_is_main'),
        'page', 'image_title', 'image_description')


@admin.register(PageComment)
class PageCommentAdmin(DefaultSettings):
    menu_title = "Страница:Комментарии"
    menu_group = "Пользователи"
    raw_id_fields = ('page', 'user')
    date_hierarchy = 'created'
    search_fields = ('username', 'page__title', 'text')
    list_display = ('email', 'page', 'text', 'user', 'is_show')
    list_display_links = ('email', 'page')
    list_editable = ('is_show',)
    list_filter = (
        'is_show',
        ('created', DateRangeFilter), ('updated', DateRangeFilter)
    )
