from __future__ import unicode_literals
from django.contrib import admin
from django.shortcuts import render
from daterange_filter.filter import DateRangeFilter
from utils.abstract_admin import DefaultSettings
from order.models import Order, OrderItem, Status, Story


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product_item', )
    extra = 0


class StoryInline(admin.TabularInline):
    model = Story
    readonly_fields = ('total_cost', 'status', 'comment', 'created', 'updated')
    extra = 0
    classes = ('collapse',)
    # закоментровать когда в продакшен уйдет -
    # can_delete = None
    ordering = ('-created',)


@admin.register(Status)
class StatusAdmin(DefaultSettings):
    menu_title = 'Заказы: Статусы заказов'
    menu_group = 'Заказы'
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(DefaultSettings):
    menu_title = 'Заказы'
    menu_group = 'Заказы'
    search_fields = ('id', 'email', 'last_name')
    date_hierarchy = 'created'
    actions = ('go_print',)
    raw_id_fields = ('user',)
    list_filter = (
        'status',
        ('created', DateRangeFilter), ('updated', DateRangeFilter),
        'city'
    )
    list_display = ('id', 'user', 'email', 'city', 'total_cost', 'status', 'created')
    list_display_links = ('id', 'user')

    inlines = (OrderItemInline, StoryInline)
    readonly_fields = ('id', 'created', 'total_cost')
    fields = (('id', 'user', 'status'), 'total_cost', 'last_name', 'first_name', 'address', 'postal_code', 'city', 'ttn',
              'comment', 'created',)

    def go_print(self, request, queryset):
        """
        Создать табличный вид объекта и выставить на печать
        ? поля текщей модели обекта - заголовкок таблицы, и значения
        ? Отдать сверстанную таблицу в ХТМЛ шаблон с кнопкой "Печать"
        ? Кнопку обрабатывает JS 'print()' - вывести на печать
        """
        return render(request, 'order/templates/go_print.html', context={'order': queryset.first()})
    go_print.short_description = 'Распечатать'


@admin.register(Story)
class StoryAdmin(DefaultSettings):
    menu_title = 'Заказы: Истории заказов'
    menu_group = 'Заказы'
    date_hierarchy = 'created'
    search_fields = ('order_id', 'status')
    list_filter = (
        'status',
        ('created', DateRangeFilter), ('updated', DateRangeFilter),
    )
    list_display = ('order', 'status', 'total_cost', 'created', 'comment')
    raw_id_fields = ('order',)
