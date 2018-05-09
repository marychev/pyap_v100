from django.contrib import admin
from mptt.admin import TreeRelatedFieldListFilter
from utils.abstract_admin import ABSMPTTContentSeoAdmin, ImageInlineTabularAdmin
from .models import Catalog, CatalogImage


# INLINE ---

class CatalogImageInline(ImageInlineTabularAdmin):
    model = CatalogImage

# --------------------------------------------


@admin.register(Catalog)
class CatalogAdmin(ABSMPTTContentSeoAdmin):
    menu_title = "Каталог"
    menu_group = "Каталог"

    inlines = (CatalogImageInline,)
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
