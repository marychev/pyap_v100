from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from filebrowser.models import FileBrowser
from filebrowser.settings import SHOW_IN_DASHBOARD
from site_info.models import TextInfo, ListLink
from utils.abstract_admin import DefaultSettings


admin.site.unregister(FileBrowser)


class FileBrowserAdmin(DefaultSettings):
    menu_title = 'Медиа-файлы'
    menu_group = 'Медиа'
    actions = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        opts = self.model._meta
        info = opts.app_label, (opts.model_name if hasattr(opts, 'model_name') else opts.module_name)
        return [
            url('^$', self.admin_site.admin_view(self.filebrowser_view), name='{0}_{1}_changelist'.format(*info)),
        ]

    def filebrowser_view(self, request):
        return HttpResponseRedirect(reverse('filebrowser:fb_browse'))


if SHOW_IN_DASHBOARD:
    admin.site.register(FileBrowser, FileBrowserAdmin)

# ------------------------------------------------------------------------------------


@admin.register(TextInfo)
class TextInfoAdmin(DefaultSettings):
    menu_title = '4.Текстовая информация'
    menu_group = 'Настройки'
    search_fields = ('title',)
    list_display = ('title', 'get_html')
    list_filter = ('title',)


@admin.register(ListLink)
class ListLinkAdmin(DefaultSettings):
    menu_title = '5.Быстрые ссылки'
    menu_group = 'Настройки'
    search_fields = ('title',)
    list_display = ('title', 'url', 'is_show', 'type_link')
    list_editable = ('type_link', 'url', 'is_show')
    list_filter = ('type_link', 'is_show')
    fields = (('title', 'is_show'), 'sort', 'url', 'type_link')





