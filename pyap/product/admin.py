from django.contrib import admin, messages
from django.utils.html import format_html
from mptt.admin import TreeRelatedFieldListFilter
from sorl.thumbnail.admin import AdminImageMixin
from daterange_filter.filter import DateRangeFilter
from utils.abstract_admin import DefaultSettings, ImageInlineTabularAdmin, ImageAdmin, SEOAdmin
from .models import Product, ProductImage, ProductItem, ProductComment


# INLINE ---

class ProductImageInline(ImageInlineTabularAdmin):
    model = ProductImage


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    show_change_link = True
    extra = 0

# ================================


@admin.register(Product)
class ProductAdmin(ImageAdmin, SEOAdmin):
    menu_title = "Товар"
    menu_group = "Каталог"
    # list_max_show_all = 500
    # ------------------------------------------------------------------------
    # заменить стандартные  размеры input, textarea
    # formfield_overrides = {
    #     # models.CharField: {'widget': TextInput(attrs={'size': '60'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows': 6})},
    # }
    # class Media:
    #     """заменяет стандартный select на checkbox при мульти-выборе"""
    #     js = ['admin/js/mselect-to-mcheckbox.js']
    #     css = {'all': ('admin/css/mselect-to-mcheckbox.css',)}
    # ---------------------------------------------------------------------

    actions = ['clone_object'] + SEOAdmin.abs_actions
    readonly_fields = ImageAdmin.abs_readonly_fields + SEOAdmin.abs_readonly_fields
    inlines = (ProductImageInline, ProductItemInline)

    filter_horizontal = ('catalog', 'recommend_products')
    search_fields = ('title', 'articul')
    list_filter = (
        'is_show', 'is_bestseller', 'is_new', ('catalog', TreeRelatedFieldListFilter),
        ('created', DateRangeFilter), ('updated', DateRangeFilter)
    )
    list_display = ('get_image_thumb', 'get_price', 'title', 'articul', 'is_show', 'is_bestseller', 'is_new', 'sort')
    list_display_links = ('get_image_thumb', 'get_price', 'title')
    list_editable = ('sort', 'is_show', 'is_bestseller', 'is_new')

    fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {
            'fields': (
                ('get_image_thumb', 'is_bestseller', 'is_new'),
                SEOAdmin.abs_fieldsets, 'articul', 'catalog', 'recommend_products',
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

    def clone_object(self, request, queryset):
        """Копирование(клонирование) выбранных объектов - action"""
        for obj in queryset:
            prefix = '-_CLONE'
            catalogs = obj.catalog.all()
            clone = obj
            clone.title += prefix
            if clone.articul:
                clone.articul += prefix
            clone.slug += prefix
            clone.description += prefix
            clone.seo_title = clone.seo_description = clone.seo_keywords = ''
            clone.id = None
            clone.save()
            [clone.catalog.add(c) for c in catalogs]
            messages.success(request, format_html('Склонирован <b>{}</b>', obj))
    clone_object.short_description = 'Клонировать'

    def get_price(self, obj):
        return obj.get_price()
    get_price.short_description = 'Цена'

    # --------------------------------------------------------------------------------------------
    # # это что бы при добавлении/изменении рубрики список выбора из поля parent был в виде дерева
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     field = super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #     if db_field.title == 'parent':
    #         field.choices = [('', '---------')]
    #         for rubric in Catalog.objects.all():
    #             field.choices.append((rubric.pk, '+--'*(rubric.level) + rubric.title))
    #     return field
    # --------------------------------------------------------------------------------------------

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name in 'recommend_products':
    #
    #         print(self.get_queryset(request))
    #         current_obj = self.get_queryset(request)
    #         print(kwargs)
    #     return super(ProductAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(ProductItem)
class ProductItemAdmin(DefaultSettings):
    menu_title = "..Товар:Варианты"
    menu_group = "Каталог"
    actions = ('clone_object',)
    raw_id_fields = ('product',)
    search_fields = ('articul', 'name', 'product__articul', 'product__title')
    date_hierarchy = 'created'
    prepopulated_fields = {'articul': ('name',)}
    list_display = ('name', 'articul', 'product', 'price', 'price_discount', 'price_purchase', 'quantity', 'is_main')
    list_editable = ('price', 'price_discount', 'price_purchase', 'quantity', 'is_main')
    list_display_links = ('name', 'articul', 'product')
    list_filter = (
        'is_main',
        ('created', DateRangeFilter), ('updated', DateRangeFilter),
        ('product__catalog', TreeRelatedFieldListFilter)
    )

    def clone_object(self, request, queryset):
        """Копирование(клонирование) выбранных объектов - action"""
        prefix = '-_CLONE'
        for obj in queryset:
            name = obj.name if obj.name else str(obj.id)
            articul = obj.articul if obj.articul else 'art_' + str(obj.id)
            clone = obj
            clone.name = name + prefix
            clone.articul = articul + prefix
            clone.id = None
            clone.is_main = False
            clone.save()
            messages.success(request, format_html('Склонирован <b>{}</b>', obj))
    clone_object.short_description = 'Клонировать'


@admin.register(ProductImage)
class ProductImageAdmin(AdminImageMixin, ImageAdmin):
    menu_title = "..Товар:Фотографии"
    menu_group = "Каталог"
    raw_id_fields = ('product',)
    search_fields = ('product__title', 'product__articul')
    fields = ('product', 'image')
    list_display = ('__str__', 'get_thumbnail_html')
    list_display_links = ('__str__',)
    list_filter = ('product__catalog',)


@admin.register(ProductComment)
class ProductCommentAdmin(DefaultSettings):
    menu_title = "..Товар:Комментарии"
    menu_group = "Пользователи"
    raw_id_fields = ('product', 'user')
    date_hierarchy = 'created'
    search_fields = ('username', 'product__title', 'text')
    list_display = ('email', 'product', 'text', 'user', 'is_show')
    list_display_links = ('email', 'product')
    list_editable = ('is_show',)
    list_filter = (
        'is_show',
        ('created', DateRangeFilter), ('updated', DateRangeFilter)
    )



# class MyTreeRelatedFieldListFilter(TreeRelatedFieldListFilter):
#     """Отступы правого фильтра для категорий"""
#     mptt_level_indent = 20


