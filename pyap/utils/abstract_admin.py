from django.contrib import admin, messages
from django.utils.html import format_html
from utils.thumbnail import get_thumb
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter


class DefaultSettings(admin.ModelAdmin):
    """
    Стандартные настройки для всех классов
    """
    empty_value_display = '- нет -'
    save_on_top = True
    abs_actions = ['clone_object']

    def get_html(self, obj):
        """
        Вернуть ХТМЛ из строки `<object>.html`
        """
        from django.utils.html import format_html
        return format_html(obj.html)
    get_html.short_description = 'HTML'

    def todo_dev(self, request):
        return '[!]' + str(self)

    def clone_object(self, request, queryset):
        """Копирование(клонирование) выбранных объектов - action"""
        for obj in queryset:
            prefix = '-_CLONE'
            clone = obj
            clone.title += prefix
            clone.slug += prefix
            clone.seo_title = clone.seo_description = clone.seo_keywords = ''
            clone.id = None
            clone.is_show = False
            clone.save()
            messages.success(request, format_html('Склонирован <b>{}</b>', obj))
    clone_object.short_description = 'Клонировать'


# - IMAGES -------

class ImageInlineTabularAdmin(admin.TabularInline):
    # _readonly_fields = ('get_thumbnail_html',)
    show_change_link = True
    extra = 0
    classes = ('collapse',)

    def get_thumbnail_html(self, obj):
        return get_thumb(obj.image)
    get_thumbnail_html.short_description = 'Текущее фото'


class ImageAdmin(DefaultSettings):
    """
    Абстрактный класс для изображений в админке.
    """
    abs_readonly_fields = ['get_image_thumb']
    abs_actions = ['set_watermark']

    def get_thumbnail_html(self, obj):
        """
        Получить миниатюру.
        Для обекта с параметром: ``image {FileBrowser}``
        """
        return get_thumb(obj.image)
    get_thumbnail_html.short_description = 'Рис .'

    def get_image_thumb(self, obj):
        """
         Аналогичен ``get_thumbnail_html()``, но принимате целый обект
         с параметрами и Методом:`get_main_image()`, который отдает данные:
            obj.<<object>>: QuerySet
            obj.get_main_image().image: ImageObject
            obj.get_main_image().image_is_main: bool
            obj.get_main_image().image_title: string
            obj.get_main_image().image_description: text
        """
        if obj.get_main_image():
            image = obj.get_main_image().image
            return get_thumb(image)
    get_image_thumb.short_description = 'Рис.'

    def set_watermark(self, request, queryset):
        """
        Обновить/добавить данные из файла CSV
            *если sorl.thumbnail чистим кэш: >>_ python manage.py thumbnail clear_delete_all
            *перезапускаем проект
        """
        from utils.thumbnail import add_watermark
        from django.conf import settings
        from PIL import Image

        # Открыть водяной знак
        watermark = Image.open(settings.WATERMARK_IMG, 'r')
        for query in queryset:
            if query.image:
                img_path = settings.BASE_DIR + query.image.url  # Открываем текущее изображение
                img_open = Image.open(img_path, 'r')
                print('{}: {}'.format('action `set_watermark`',
                                      add_watermark(img_open, watermark).save(img_path)))  # NOTE: print(!)
    set_watermark.short_description = 'Наложить водяной знак ``../static/images/logo.png``'


class ImageMPTTModelAdmin(MPTTModelAdmin):
    get_readonly_fields = ('get_thumbnail_html',)

    def get_thumbnail_html(self, obj):
        return get_thumb(obj.image)
    get_thumbnail_html.short_description = 'Текущее фото'

# --------------------------------------------------------------------


class SEOAdmin(DefaultSettings):
    """
    Настройка по умолчанию для СЕО полей
    """
    prepopulated_fields = {'slug': ('title',)}
    view_on_site = True

    abs_actions = ['fill_seo_fields']
    abs_fields = ['slug', 'seo_title', 'seo_description', 'seo_keywords', 'og_locale', 'scripts']
    abs_fieldsets = 'title', 'is_show', 'description', 'html',
    abs_readonly_fields = ['created', 'updated']

    def fill_seo_fields(self, request, queryset):
        """
        Заполнить сео поля. Не трогать заполненные поля.
        [*можно улучшить: model:SeoTemplate]
        """
        for query in queryset:
            default_title = query.title
            if not query.seo_title:
                query.seo_title = default_title
            if not query.seo_description:
                query.seo_description = default_title
            if not query.seo_keywords:
                query.seo_keywords = default_title
            query.save()
    fill_seo_fields.short_description = 'Заполнить SEO поля(пустые)'


class ABSContentSeoAdmin(ImageAdmin, SEOAdmin):
    """
    Абстракный клас. Включает настройки Сео и Контент полей.
    """
    abs_actions = ImageAdmin.abs_actions + SEOAdmin.abs_actions + ['clone_object']
    abs_raw_id_fields = ('author',)
    abs_readonly_fields = ('get_image_thumb', 'created', 'updated')
    abs_search_fields = ('title',)
    abs_list_filter = ('is_show', 'is_allow_comments', 'tags')
    abs_list_display = ('title', 'get_image_thumb', 'author', 'sort', 'is_show', 'is_allow_comments',)
    abs_list_display_links = ('title', 'get_image_thumb', 'author')
    abs_list_editable = ('sort', 'is_show', 'is_allow_comments')
    abs_fieldsets_fields = SEOAdmin.abs_fields
    abs_fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {
            'fields': (
                'get_image_thumb', ('title', 'is_show'), 'description', 'html', 'sort',
                'author', 'is_allow_comments', 'tags'
            ),
        }),
        ('СЕО-НАСТРОЙКИ', {
            'classes': ('collapse',),
            'fields': abs_fieldsets_fields,
        }),
        ('ИНФОРМАНЦИЯ', {
            'classes': ('collapse',),
            'fields': abs_readonly_fields,
        }),
    )


class ABSMPTTContentSeoAdmin(MPTTModelAdmin, ImageAdmin, SEOAdmin):
    """
    Абстракный клас. Включает настройки MPTTModeAdmin, Сео и Контент полей.
    """
    mptt_level_indent = 23
    abs_actions = ImageAdmin.abs_actions + SEOAdmin.abs_actions + ['rebuild']
    abs_raw_id_fields = ('parent', 'author')
    abs_readonly_fields = ('get_image_thumb', 'created', 'updated')
    abs_search_fields = ('title', 'parent__title')
    abs_list_filter = (
        'is_show', ('parent', TreeRelatedFieldListFilter), 'tags',
    )
    abs_list_display = ('title', 'get_image_thumb', 'parent', 'author', 'sort', 'is_show')
    abs_list_display_links = ('title', 'get_image_thumb', 'author')
    abs_list_editable = ('parent', 'sort', 'is_show')
    abs_fieldsets_fields = SEOAdmin.abs_fields
    abs_fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {
            'fields': (
                'get_image_thumb', ('title', 'is_show'), 'parent', 'description', 'html',
                'sort', 'author', 'tags'
            ),
        }),
        ('СЕО-НАСТРОЙКИ', {
            'classes': ('collapse',),
            'fields': abs_fieldsets_fields,
        }),
        ('ИНФОРМАНЦИЯ', {
            'classes': ('collapse',),
            'fields': abs_readonly_fields,
        }),
    )

    def rebuild(self, request, queryset):
        """
        Пересорбать МПТТ модель. Иногда требуется для перезагрузки дерева.
        """
        self.model.objects.rebuild()
    rebuild.short_description = 'Пересобрать пункты раздела'


class ABSDefaultMPTTAdmin(MPTTModelAdmin):
    """
    Стандартные настройки для MPTT моделей
    """
    mptt_level_indent = 23

    abs_actions = ['rebuild']

    def rebuild(self, request, queryset):
        """
        Пересорбать МПТТ модель. Иногда требуется для перезагрузки дерева.
        """
        self.model.objects.rebuild()
    rebuild.short_description = 'Пересобрать пункты раздела'
