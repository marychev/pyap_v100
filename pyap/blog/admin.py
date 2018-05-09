from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from utils.abstract_admin import ImageAdmin, ImageInlineTabularAdmin, DefaultSettings, \
    ABSMPTTContentSeoAdmin, ABSContentSeoAdmin
from .models import Blog, BlogImage, Post, PostImage, Comment


# INLINE ---

class BlogImageInline(ImageInlineTabularAdmin):
    model = BlogImage


class PostImageInline(ImageInlineTabularAdmin):
    model = PostImage

# --------------------------------------------


@admin.register(Blog)
class BlogAdmin(ABSMPTTContentSeoAdmin):
    menu_title = "Блог"
    menu_group = "Контент"
    inlines = (BlogImageInline,)
    action = (ABSMPTTContentSeoAdmin.abs_actions,)
    raw_id_fields = ABSMPTTContentSeoAdmin.abs_raw_id_fields
    filter_horizontal = ('tags',)
    readonly_fields = ABSMPTTContentSeoAdmin.abs_readonly_fields
    search_fields = ABSMPTTContentSeoAdmin.abs_search_fields
    list_filter = ABSMPTTContentSeoAdmin.abs_list_filter
    list_display = ABSMPTTContentSeoAdmin.abs_list_display
    list_display_links = ABSMPTTContentSeoAdmin.abs_list_display_links
    list_editable = ABSMPTTContentSeoAdmin.abs_list_editable
    fieldsets = ABSMPTTContentSeoAdmin.abs_fieldsets


@admin.register(BlogImage)
class BlockImageAdmin(ImageAdmin):
    menu_title = "Блог:Фото"
    menu_group = "Контент"
    raw_id_fields = ('blog',)
    search_fields = ('image_title', 'blog__title')
    list_filter = ('image_is_main', 'blog')
    list_display = ('get_thumbnail_html', 'blog', 'image_title', 'image_description', 'image_is_main')
    list_editable = ('image_title', 'image_is_main')
    list_display_links = ('get_thumbnail_html', 'blog')
    fields = (
        ('image', 'image_is_main'),
        'blog', 'image_title', 'image_description')


@admin.register(Post)
class PostAdmin(ABSContentSeoAdmin):
    menu_title = "Блог:Посты"
    menu_group = "Контент"
    inlines = (PostImageInline,)
    action = (ABSContentSeoAdmin.abs_actions,)
    raw_id_fields = ('blog',) + ABSContentSeoAdmin.abs_raw_id_fields
    filter_horizontal = ('tags',)
    readonly_fields = ABSContentSeoAdmin.abs_readonly_fields + ('comment_count',)
    search_fields = ABSContentSeoAdmin.abs_search_fields
    list_filter = ('blog',) + ABSContentSeoAdmin.abs_list_filter
    list_display = ('blog',) + ABSContentSeoAdmin.abs_list_display
    list_display_links = ('blog',) + ABSContentSeoAdmin.abs_list_display_links
    list_editable = ABSContentSeoAdmin.abs_list_editable

    custom_fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {
            'fields': (
                'blog', 'get_image_thumb', ('title', 'is_show'), 'description', 'html', 'is_allow_comments',
                'author', 'tags', 'sort',
            ),
        }),
        ('СЕО-НАСТРОЙКИ', {
            'classes': ('collapse',),
            'fields': ABSContentSeoAdmin.abs_fieldsets_fields,
        }),
        ('ИНФОРМАНЦИЯ', {
            'classes': ('collapse',),
            'fields': readonly_fields,
        }),
    )
    fieldsets = custom_fieldsets


@admin.register(PostImage)
class PostImageAdmin(ImageAdmin):
    menu_title = "Посты:Фото"
    menu_group = "Контент"
    raw_id_fields = ('post',)
    search_fields = ('image_title', 'post__title')
    list_filter = ('image_is_main', 'post')
    list_display = ('get_thumbnail_html', 'post', 'image_title', 'image_description', 'image_is_main')
    list_editable = ('image_title', 'image_is_main')
    list_display_links = ('get_thumbnail_html', 'post')
    fields = (
        ('image', 'image_is_main'),
        'post', 'image_title', 'image_description')


@admin.register(Comment)
class CommentAdmin(DefaultSettings):
    menu_title = "Блог:Комментарии"
    menu_group = "Пользователи"
    raw_id_fields = ('post', 'user')
    date_hierarchy = 'created'
    search_fields = ('username', 'post__title', 'text')
    list_display = ('email', 'post', 'text', 'user', 'is_show')
    list_display_links = ('email', 'post')
    list_editable = ('is_show',)
    list_filter = (
        'is_show',
        ('created', DateRangeFilter), ('updated', DateRangeFilter)
    )
