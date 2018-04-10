from django.contrib import admin
from utils.abstract_admin import DefaultSettings
from .models import HTMLTemplate, SentLetter


@admin.register(HTMLTemplate)
class HTMLTemplateAdmin(DefaultSettings):
    menu_title = "Емайл сообщения"
    menu_group = "Настройки"
    search_fields = ('event',)
    list_filter = ('event', 'is_admin')
    list_display = ('event', 'is_admin', 'to_email')
    actions = ('sent_custom',)

    def sent_custom(self, request, queryset):
        """Отправить письма, с Индивидуальным шаблоном"""
        for query in queryset:
            query.sent()
    sent_custom.short_description = 'Отправить письма'


@admin.register(SentLetter)
class SentLetterAdmin(DefaultSettings):
    menu_title = "Отправленные сообщения"
    menu_group = "Настройки"
    date_hierarchy = 'created_at'
    search_fields = ('html_template__to_email', 'html_template__subject')
    list_filter = ('is_sent', 'created_at', 'updated_at')
    list_display = ('html_template', 'order', 'user', 'is_sent', 'created_at')
    readonly_fields = ('get_html',)
    raw_id_fields = ('order', 'user', 'coupon', 'html_template')
    fields = ('order', 'user', 'coupon', 'html_template', 'is_sent', 'get_html')

